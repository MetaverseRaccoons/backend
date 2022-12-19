from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_learner = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    national_registration_number = models.CharField(max_length=15, blank=True, null=True)
    has_drivers_license = models.BooleanField(default=False)
    is_shareable = models.BooleanField(default=False)
    friends = models.ManyToManyField('User', blank=True)

class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
