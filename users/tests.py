from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfileModel

class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = '/users/login/'
        self.profile_url = reverse('profile')
        self.refresh_url = reverse('refresh')
        self.logout_url = reverse('logout')
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_user(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "password123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def authenticate(self):
        user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return user

    def test_get_profile_authenticated(self):
        user = self.authenticate()
        profile = UserProfileModel.objects.create(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        user = self.authenticate()
        profile = UserProfileModel.objects.create(user=user)
        payload = {
            "fullname": "Test User", 
            "address": "Test address",
            "mobilenumber": "1234567890",
            "geneder": "M",
        }
        response = self.client.put(self.profile_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fullname'], "Test User")
        self.assertEqual(response.data['address'], "Test address")
        self.assertEqual(response.data['mobilenumber'], "1234567890")
        self.assertEqual(response.data['geneder'], "M")

    def test_token_refresh(self):
        user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(user)
        response = self.client.post(self.refresh_url, {"refresh": str(refresh)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout(self):
        user = self.authenticate()
        refresh = RefreshToken.for_user(user)
        response = self.client.post(self.logout_url, {"refresh": str(refresh)}, format='json')
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
