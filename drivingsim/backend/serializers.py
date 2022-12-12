from rest_framework import serializers

from .models import User


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