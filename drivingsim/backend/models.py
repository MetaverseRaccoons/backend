from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F


class User(AbstractUser):
    is_learner = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    national_registration_number = models.CharField(max_length=15, blank=True, null=True)
    has_drivers_license = models.BooleanField(default=False)
    is_shareable = models.BooleanField(default=False)

    def get_friends(self):
        return Friends.objects.filter(Q(from_user=self) | Q(to_user=self), accepted=True)

    def get_friend_requests(self):
        return Friends.objects.filter(Q(to_user=self), accepted=False)

    def get_friends_and_friend_requests(self):
        return Friends.objects.filter((Q(from_user=self) & Q(accepted=True)) | Q(to_user=self))

    def is_friend(self, user):
        return self.get_friends().filter(Q(from_user=user) | Q(to_user=user)).exists()


class Friends(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    accepted = models.BooleanField(default=False)

    class Meta:
        # Problem: we can still create duplicate friend requests in opposite directions
        # eg FriendRequest(user1, user2) and FriendRequest(user2, user1) can both exist right now
        constraints = [
            models.CheckConstraint(check=~Q(from_user=F('to_user')), name='no_self_friendships'),
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_friend_request'),
        ]


