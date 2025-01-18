from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from authentication.views import register_user  # Update the import path as needed
from authentication.serializers import UsersSerializer  # Update the serializer name/path
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/register/'

    def test_register_user_success(self):
        # Prepare the payload with only email and password
        payload = {
            "email": "testuser@example.com",
            "password": "securepassword"
        }

        # Create a POST request
        request = self.factory.post(self.url, payload, format='json')

        # Call the view directly
        response = register_user(request)

        # Assert the expected response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "user registered successfully")
        self.assertEqual(response.data['data']['email'], "testuser@example.com")

    def test_register_user_missing_field(self):
        # Missing password in the payload
        payload = {
            "email": "testuser@example.com"
        }

        # Create a POST request
        request = self.factory.post(self.url, payload, format='json')

        # Call the view directly
        response = register_user(request)

        # Assert the expected response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "error while registration")
        self.assertIn('password', response.data['errors'])

    def test_register_user_invalid_email(self):
        # Invalid email in the payload
        payload = {
            "email": "invalid-email",
            "password": "securepassword"
        }

        # Create a POST request
        request = self.factory.post(self.url, payload, format='json')

        # Call the view directly
        response = register_user(request)

        # Assert the expected response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "error while registration")
        self.assertIn('email', response.data['errors'])

    def test_register_user_internal_server_error(self):
        # Simulate a scenario that causes an exception (e.g., database error)
        payload = {
            "email": "testuser@example.com",
            "password": "securepassword"
        }

        # Temporarily mock the save method to raise an exception
        original_save = UsersSerializer.save
        def mock_save(*args, **kwargs):
            raise Exception("Database error")
        UsersSerializer.save = mock_save

        # Create a POST request
        request = self.factory.post(self.url, payload, format='json')

        # Call the view directly
        response = register_user(request)

        # Restore the original save method
        UsersSerializer.save = original_save

        # Assert the expected response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], "Internal Server Error")
        self.assertIn("Database error", response.data['errors'])
