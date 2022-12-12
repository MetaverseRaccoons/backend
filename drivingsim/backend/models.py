from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_learner = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    national_registration_number = models.CharField(max_length=15, blank=True, null=True)
    has_drivers_license = models.BooleanField(default=False)
    is_shareable = models.BooleanField(default=False)

