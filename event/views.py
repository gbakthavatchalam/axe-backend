from django.shortcuts import render
from rest_framework import viewsets
from event.models import Event, User, Acceptance
from event.serializers import UserSerializer, EventSerializer, EventResponseSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventAcceptanceViewSet(viewsets.ModelViewSet):
    queryset = Acceptance.objects.all()
    serializer_class = EventResponseSerializer

