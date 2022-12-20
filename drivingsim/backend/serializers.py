from rest_framework import serializers
from .models import User, Friends


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
        ]


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = [
            'from_user',
            'to_user',
            'accepted',
        ]
