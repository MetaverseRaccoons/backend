from rest_framework import serializers
from .models import User, Friends, Violation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'is_learner',
            'is_instructor',
            'has_drivers_license',
            'is_shareable',
            'km_driven',
            'minutes_driven',
        ]


class FriendsSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Friends
        fields = [
            'from_user',
            'to_user',
            'accepted',
        ]


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = [
            'time',
            'type',
            'severity',
            'description',
        ]
