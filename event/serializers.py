from event.models import User, Event, Acceptance
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('display_name', 'mobile', 'is_active')
        read_only_fields = ('is_active',)

    def create(self, validated_data):
        validated_data['is_active'] = 0 # During user creation, they are inactive. Only upon OTP verification, users are activated
        print(validated_data)
        return super(UserSerializer, self).create(validated_data)

    def validate_mobile(self, value):
        if not len(str(value)) == 10:
            raise serializers.ValidationError('This field must be of length 10')
        return value


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'host')
        read_only_fields = ('host',)

    def create(self, validated_data):
        validated_data['host'] = User.objects.get(mobile='9710257197')
        return super(EventSerializer, self).create(validated_data)


class EventResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceptance
        fields = ('event_id', 'response', 'participant')

    def create(self, validated_data):
        validated_data['response'] = None
        return super(EventResponseSerializer, self).create(validated_data)
