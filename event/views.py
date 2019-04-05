from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from event.models import Event, AuthUser, Acceptance
from event.serializers import (
    EventSerializer,
    EventResponseSerializer,
    SignUpSerializer
)


hasher = PBKDF2PasswordHasher()

# Create your views here.


class EventViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'patch', 'delete', 'get', 'put')
    permission_classes = (IsAuthenticated,)

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def _translate_host(self, request):
        if 'host' in request.data:
            request.data['host'] = AuthUser.objects.get(username=request.data['host']).id

    def create(self, request, *args, **kwargs):
        try:
            self._translate_host(request)
        except (KeyError, ValueError) as e:
            return HttpResponseServerError(content=b'Invalid Host')
        return super(EventViewSet, self).create(request, *args, **kwargs)


class EventAcceptanceViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'patch', 'delete')
    permission_classes = (IsAuthenticated,)

    queryset = Acceptance.objects.all()
    serializer_class = EventResponseSerializer
    lookup_field = 'event_id'

    def create(self, request, *args, **kwargs):
        try:
            participants_data = request.data.pop('participants')
        except:
            participants_data = []

        for participant in participants_data:
            participant_id = AuthUser.objects.get(username=participant)
            Acceptance.objects.get_or_create(
                event_id=request.data['event_id'],
                response=0,
                participant=participant_id
            )
        return Response(data={"message": "ok"})

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            request.data['participant'] = AuthUser.objects.get(username=request.data['participant']).id
            filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field], 'participant': request.data['participant']}
            instance = get_object_or_404(self.queryset, **filter_kwargs)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except Exception as e:
            return HttpResponseServerError(content=e)

    def destroy(self, request, *args, **kwargs):
        try:
            participants_data = request.data.pop('participants')
        except:
            participants_data = []

        for participant in participants_data:
            participant_id = AuthUser.objects.get(username=participant)
            filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field], 'participant': participant_id}
            instance = get_object_or_404(self.queryset, **filter_kwargs)
            instance.delete()
        return Response(data={"message": "ok"})


class SignUpViewSet(viewsets.ModelViewSet):
    """Has custom authentication. For password updation, authentication is done through OTP process.
    For other profile detail update, a valid token is required
    """
    http_method_names = ('post', 'patch', 'get')

    queryset = AuthUser.objects.all()
    serializer_class = SignUpSerializer
    lookup_field = 'username'

    def list(self, *args, **kwars):
        return HttpResponseServerError(content=b'Not Implemented')

    def retrieve(self, request, *args, **kawrgs):
        if isinstance(request.user, AnonymousUser):
             return Response(status=401, data={"message": "Invalid authorization"})
        return super(SignUpViewSet, self).retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Allow update of password and is_active without Authorization
        For reset password, the user is authorized through an OTP
        For """
        if 'password' in request.data:
            request.data['password'] = hasher.encode(password=request.data['password'],
                                            salt='salt',
                                            iterations=50000)
        elif 'is_active' in request.data:
            pass
        else:
            # Authenticate the API for updating profile details other than password, is_active
            if isinstance(request.user, AnonymousUser):
                 return Response(status=401, data={"message": "Invalid authorization"})
        return super(SignUpViewSet, self).partial_update(request, *args, **kwargs)
