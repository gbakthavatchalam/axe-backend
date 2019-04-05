from collections import OrderedDict
import datetime
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from event.models import AuthUser, Event, Acceptance
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


hasher = PBKDF2PasswordHasher()


class EventResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceptance
        fields = ('response', 'participant')

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.field_name in ('participant', 'host'):
                    try:
                        ret[field.field_name] = AuthUser.objects.get(id=attribute.pk).username
                    except:
                        ret[field.field_name] = field.to_representation(attribute)
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret


class EventSerializer(serializers.ModelSerializer):
    participants = EventResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'host', 'location', 'participants')

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.field_name in ('participant', 'host'):
                    try:
                        ret[field.field_name] = AuthUser.objects.get(id=attribute.pk).username
                    except:
                        ret[field.field_name] = field.to_representation(attribute)
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('username', 'first_name', 'last_name', 'display_name', 'email', 'password', 'is_active')

    @property
    def _readable_fields(self):
        return [
            field for field_name, field in self.fields.items()
            if not field.write_only and field_name != 'password'
        ]

    def create(self, validated_data):
        validated_data['display_name'] = validated_data['first_name'] + ' ' + validated_data['last_name']
        validated_data['is_superuser'] = 0
        validated_data['is_staff'] = 0
        validated_data['is_active'] = 1
        validated_data['date_joined'] = datetime.datetime.now()
        validated_data['password'] = hasher.encode(password=validated_data['password'],
                                        salt='salt',
                                        iterations=50000)
        return super(SignUpSerializer, self).create(validated_data)
