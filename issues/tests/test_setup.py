from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.tests.test_utils import generate_test_image
from issues.models import Category

User = get_user_model()


class TestSetup(APITestCase):

    def setUp(self):

        image = generate_test_image('profile_image')

        self.create_list_category_url = reverse('category-list')

        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="Password123!",
            first_name="Test1",
            middle_name="B",
            last_name="User",
            bio="This is a sample test user for unit testing.",
            address="123 Test Street, Kathmandu, Nepal",
            profile_image= image,
            phone_number="+97798000110000"
        )

        self.admin = User.objects.create_user(
            email="test1@gmail.com",
            password="Password123!",
            first_name="admin",
            middle_name="B",
            last_name="User",
            bio="This is a sample test user for unit testing.",
            address="123 Test Street, Kathmandu, Nepal",
            profile_image=image,
            phone_number="+97798000111100",
            is_staff=True
        )

        self.categories = []

        for i in range(5):

            category = Category.objects.create(
                name=f'Electronics{i}',
                description=f'Category for electronic items like phones, laptops, and accessories{i}.'
            )
            self.categories.append(category)

        self.client=APIClient()

    def authenticate(self,user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")