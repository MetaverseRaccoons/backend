from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.

class CreateUserTest(APITestCase):
    global refresh
    global access
    
    def test_create_user(self):
        url = reverse('user')
        data = {
            "username": "testuser",
            "password1": "password76512",
            "password2": "password76512",
            "email": "test@test.be",
            "national_registration_number": "00.00.00-000.00",
            "is_learner": False,
            "is_instructor": False,
            "has_drivers_license": False,
            "is_shareable": True,
        }
        response = self.client.post(url, data)
        refresh = response.json()['refresh']
        access = response.json()['access']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if all correct elements are in the response
        # Check if password and national_registration_number are not in the response
        for element in data:
            if element != "password1" and element != "password2" and element != "national_registration_number":
                self.assertEqual(response.json()['user'][element], data[element])
        # Check if a new user is not already in the database
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check if the user can login
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password76512'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
                
        
        
