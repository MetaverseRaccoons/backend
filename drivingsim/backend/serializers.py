import pytz
from rest_framework import serializers
from .models import User, Friends, Violation, Level, LevelSession


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


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'name',
            'description',
        ]


class BareLevelSessionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields['start_time'] = serializers.DateTimeField(default_timezone=pytz.UTC)
        self.fields['end_time'] = serializers.DateTimeField(default_timezone=pytz.UTC)
        return super().to_representation(instance)


    class Meta:
        model = LevelSession
        fields = [
            'id',
            'start_time',
            'end_time',
            'completed'
        ]


class LevelSessionWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LevelSession
        fields = [
            'id',
            'user',
            'start_time',
            'end_time',
            'completed'
        ]


class LevelSessionWithLevelSerializer(serializers.ModelSerializer):
    level = LevelSerializer()

    class Meta:
        model = LevelSession
        fields = [
            'id',
            'level',
            'start_time',
            'end_time',
            'completed'
        ]


class LevelSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = LevelSerializer()
    violations = ViolationSerializer(many=True)

    class Meta:
        model = LevelSession
        fields = [
            'id',
            'user',
            'level',
            'start_time',
            'end_time',
            'completed',
        ]


