from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class  RegisterTestCase(APITestCase):
    client = APIClient()

    def test_register(self):

        data = {
            "username": "testcase",
            "email": "testcase@test.com",
            "password": "Pass@1234",
            "password2": "Pass@1234",
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):

        self.username = "example"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Most developers use reverse() to avoid hardcoding URLs
        Token.objects.create(user=self.user)

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify a token was actually created and returned
        self.assertTrue('token' in response.data)

    def test_logout(self):

        token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(Token.objects.filter(user=self.user).exists())
