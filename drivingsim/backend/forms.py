from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, Violation


class CreateUserForm(UserCreationForm):
    is_learner = forms.BooleanField(required=False)
    is_instructor = forms.BooleanField(required=False)
    national_registration_number = forms.CharField(max_length=15, required=True)
    has_drivers_license = forms.BooleanField(required=False)
    is_shareable = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'is_learner',
            'is_instructor',
            'national_registration_number',
            'has_drivers_license',
            'is_shareable'
        )


class AddViolationForm(forms.ModelForm):
    type = forms.CharField(max_length=50)
    severity = forms.FloatField()
    description = forms.TextInput()

    class Meta:
        model = Violation
        fields = (
            'type',
            'severity',
            'description'
        )

