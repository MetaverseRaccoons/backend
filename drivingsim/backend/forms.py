from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, Violation, Certificate, LevelSession


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


class AddLevelSessionForm(forms.ModelForm):
    level_name = forms.CharField(max_length=50)
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    completed = forms.BooleanField()

    class Meta:
        model = LevelSession
        fields = (
            'start_time',
            'end_time',
            'completed'
        )


class AddCertificateForm(forms.ModelForm):
    title = forms.CharField(max_length=150)
    description = forms.Textarea()

    class Meta:
        model = Certificate
        fields = (
            'title',
            'description'
        )

