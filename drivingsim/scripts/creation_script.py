from django.contrib.auth.models import User
from backend.forms import CreateUserForm
from backend.serializers import UserSerializer

def run():
    data_testUser1 = {
        "username": "testuser1",
        "password1": "TestPass8263",
        "password2": "TestPass8263",
        "email": "testuser1@domain.com",
        "national_registration_number": "01.20.07-050.90",
        "is_learner": True,
        "is_instructor": False,
        "has_drivers_license": True,
        "is_shareable": True
    }
    
    data_testUser2 = {
        "username": "testuser2",
        "password1": "TestPass8264",
        "password2": "TestPass8264",
        "email": "testuser2@domain.com",
        "national_registration_number": "12.00.05-030.00",
        "is_learner": True,
        "is_instructor": False,
        "has_drivers_license": False,
        "is_shareable": True
    }
    
    data_testInstructor1 = {
        "username": "testinstructor1",
        "password1": "TestPass8265",
        "password2": "TestPass8265",
        "email": "testinstructor1@domain.com",
        "national_registration_number": "60.60.06-060.00",
        "is_learner": False,
        "is_instructor": True,
        "has_drivers_license": True,
        "is_shareable": True        
    }
    
    data_testInstructor2 = {
        "username": "testinstructor2",
        "password1": "TestPass8266",
        "password2": "TestPass8266",
        "email": "testinstructor2@domain.com",
        "national_registration_number": "09.30.70-210.10",
        "is_learner": False,
        "is_instructor": True,
        "has_drivers_license": True,
        "is_shareable": True
    }

    form1 = CreateUserForm(data_testUser1)
    form1.save()
    form2 = CreateUserForm(data_testUser2)
    form2.save()
    form3 = CreateUserForm(data_testInstructor1)
    form3.save()
    form4 = CreateUserForm(data_testInstructor2)
    form4.save()