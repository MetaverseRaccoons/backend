from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.

class CreateUserTest(APITestCase):
    def test_create_user(self):
        url = reverse('user')
        data = {
            "username": "testuser",
            "password1": "password987654323456789876543",
            "password2": "password987654323456789876543",
            "email": "test@test.be",
            "national_registration_number": "00.00.00-000.00",
            "is_learner": False,
            "is_instructor": False,
            "has_drivers_license": False,
            "is_shareable": True,
        }
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
