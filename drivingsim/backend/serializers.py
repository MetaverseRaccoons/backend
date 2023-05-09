from rest_framework import serializers
from .models import User, Friends, Violation, Level, LevelSession, Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'title',
            'description',
        ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'name',
            'description',
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


class LevelSessionSerializer(serializers.ModelSerializer):
    level = LevelSerializer()

    class Meta:
        model = LevelSession
        fields = [
            'level',
            'start_time',
            'end_time',
            'completed'
        ]


class UserSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True)
    level_sessions = LevelSessionSerializer(many=True)
    violations = ViolationSerializer(many=True)

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
            'certificates',
            'level_sessions',
            'violations'
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

