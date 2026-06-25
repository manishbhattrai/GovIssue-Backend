from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url=reverse('user-register')
        self.login_url=reverse('login')

        self.user = User.objects.create_user(
            email="test.user@gmail.com",
            password="TestPassword123!",
            first_name="Test",
            middle_name="A",
            last_name="User",
            bio="This is a sample test user for unit testing.",
            address="123 Test Street, Kathmandu, Nepal",
            profile_image="profile_images/test_user.jpg",
            phone_number="+9779800000000"
        )

        self.client=APIClient()
