from .test_setup import TestSetup
from .test_utils import generate_test_image
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileTest(TestSetup):

    def test_get_profile(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.profile_url,
        )

        self.assertEqual(res.status_code, 200)

        user = User.objects.get(email='test.user@gmail.com')

        self.assertFalse(user.is_admin)
        self.assertEqual(res.data['email'],user.email)
        self.assertEqual(res.data['phone_number'],user.phone_number)
        self.assertIsNotNone(res.data['profile_image'])
        self.assertIn("trust_points",res.data)
        self.assertIn("public_id",res.data)

    def test_update_profile_success(self):

        self.authenticate(self.user)

        image = generate_test_image("profile.jpg")
        payload = {
            "first_name": "John",
            "middle_name": "Michael",
            "last_name": "Doe",
            "bio": "Software developer passionate about building scalable web applications.",
            "address": "123 Main Street, Springfield, IL 62701",
            "profile_image": image
        }
        res = self.client.patch(
            self.profile_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 200)

        user = User.objects.get(email='test.user@gmail.com')
        self.assertEqual(res.data['first_name'],user.first_name)
        self.assertEqual(res.data['address'],user.address)
        self.assertIn("profile_image",res.data)

    def test_read_only_fields_update(self):

        self.authenticate(self.user)

        payload = {
            "public_id": "usr_b72d4e91",
            "email": "jane.smith@example.com",
            "phone_number": "+1-555-987-6543",
            "trust_points": 92
        }

        res = self.client.patch(
            self.profile_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code,200)
        self.user.refresh_from_db() #it fetches the latest value
        self.assertNotEqual(self.user.email,'jane.smith@example.com')
        self.assertNotEqual(self.user.trust_points, 92)

    def test_unauthenticated_user_cannot_update(self):

        payload = {
            "first_name":"Joe"
        }

        res = self.client.patch(
            self.profile_url,
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 401)

    def test_empty_patch_request(self):

        self.authenticate(self.user)

        res = self.client.patch(
            self.profile_url,
            {},
            format='multipart'
        )

        self.assertEqual(res.status_code, 200)

    def test_profile_delete(self):

        self.authenticate(self.user)
        res = self.client.delete(
            self.profile_url
        )
        self.assertEqual(res.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_unauthenticated_user_cannot_delete_profile(self):

        res = self.client.delete(
            self.profile_url
        )

        self.assertEqual(res.status_code, 401)
