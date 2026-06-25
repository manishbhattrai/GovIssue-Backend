from .test_setup import TestSetup
from django.contrib.auth import get_user_model
from .test_utils import generate_test_image


User = get_user_model()

class RegisterTest(TestSetup):

    def test_valid_register(self):
        image = generate_test_image("profile.jpg")

        payload = {
            "email": "alice.smith@gmail.com",
            "first_name": "Alice",
            "middle_name": "Marie",
            "last_name": "Smith",
            "bio": "Frontend developer passionate about UI/UX design and modern web technologies.",
            "address": "789 Lakeside Road, Pokhara, Nepal",
            "profile_image": image,
            "phone_number": "9811122233",
            "password": "AlicePass@2026",
            "confirm_password": "AlicePass@2026"
        }
        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(email="alice.smith@gmail.com").exists())


    def test_duplicate_email(self):

        image = generate_test_image("profile.jpg")
        payload = {
            "email": "test.user@gmail.com",
            "first_name": "John",
            "middle_name": "A",
            "last_name": "Doe",
            "bio": "Duplicate email test user.",
            "address": "Kathmandu, Nepal",
            "profile_image": image ,
            "phone_number": "9800000001",
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123!"
        }

        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )
        self.assertEqual(res.status_code, 400)

    def test_missing_required_fields(self):
        image = generate_test_image("profile.jpg")
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Missing required fields test.",
            "address": "Kathmandu, Nepal",
            "profile_image": image,
            "phone_number": "9800000002"
        }

        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 400)

    def test_invalid_email_format(self):
        image = generate_test_image("profile.jpg")
        payload = {
            "email": "invalid-email-format",
            "first_name": "John",
            "middle_name": "A",
            "last_name": "Doe",
            "bio": "Invalid email format test.",
            "address": "Kathmandu, Nepal",
            "profile_image": image,
            "phone_number": "9800000003",
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123!"
        }

        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 400)

    def test_password_mismatch(self):
        image = generate_test_image("profile.jpg")
        payload = {
            "email": "new.user@example.com",
            "first_name": "John",
            "middle_name": "A",
            "last_name": "Doe",
            "bio": "Password mismatch test user.",
            "address": "Kathmandu, Nepal",
            "profile_image": image,
            "phone_number": "9800000004",
            "password": "TestPassword123!",
            "confirm_password": "DifferentPassword456!"
        }

        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code,400)

    def test_password_hashed(self):

        image = generate_test_image("profile.jpg")
        payload = {
            "email": "michael.jordan@gmail.com",
            "first_name": "Michael",
            "middle_name": "Jeffrey",
            "last_name": "Jordan",
            "bio": "Backend developer specializing in Django and REST APIs.",
            "address": "321 Riverside Drive, Lalitpur, Nepal",
            "profile_image": image,
            "phone_number": "+9779823344556",
            "password": "StrongPass@2026",
            "confirm_password": "StrongPass@2026"
        }
        res = self.client.post(
            self.register_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 201)

        user = User.objects.get(email="michael.jordan@gmail.com")

        self.assertNotEqual(user.password, 'StrongPass@2026')
        self.assertTrue(user.check_password('StrongPass@2026'))