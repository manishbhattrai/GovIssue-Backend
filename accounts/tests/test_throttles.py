from .test_setup import TestSetup
from .test_utils import generate_test_image


class ThrottleTest(TestSetup):

    def test_login_throttle(self):

        payload = {
            "email":"test@gmail.com",
            "password":"wrongpassword123"
        }

        for _ in range(5):
            res = self.client.post(
                self.login_url,
                payload,
                format='json'
            )

        res = self.client.post(
            self.login_url,
            payload,
            format='json'
        )

        self.assertEqual(res.status_code,429)
        self.assertIn("detail",res.data)

    def test_register_throttle(self):

        for i in range(4):
            image = generate_test_image('profile.jpg')
            payload = {
            "email": f"unique.user{i}@example.com",
            "first_name": f"Unique{i}",
            "middle_name": "D",
            "last_name": "Three",
            "bio": "Another test user for API and throttle testing.",
            "address": "Pulchowk, Lalitpur, Nepal",
            "profile_image": image,
            "phone_number": f"+977980300000{i}",
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123!"
            }


            res = self.client.post(
                self.register_url,
                payload,
                format='multipart'
            )
        new_image = generate_test_image('profile.jpg')
        res = self.client.post(
            self.register_url,
            {
                "email": "unique.user9@example.com",
                "first_name": "Unique",
                "middle_name": "D",
                "last_name": "Three",
                "bio": "Another test user for API and throttle testing.",
                "address": "Pulchowk, Lalitpur, Nepal",
                "profile_image": new_image,
                "phone_number": "+9779800040009",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!"
            },
            format='multipart'
        )

        self.assertEqual(res.status_code,429)
        self.assertIn("detail",res.data)

    def test_get_profile_throttle(self):
        self.authenticate(self.user)

        for _ in range(50):
            res = self.client.get(
                self.profile_url
            )

        res = self.client.get(
            self.profile_url
        )

        self.assertEqual(res.status_code, 429)
        self.assertIn("detail", res.data)

    def test_update_profile_throttle(self):

        self.authenticate(self.user)

        for i in range(12):

            payload = {
                "first_name":f"Joe{i}",
                "address":f"btm{i}"
            }

            res = self.client.patch(
                self.profile_url,
                payload,
                format='multipart'
            )


        res = self.client.patch(
            self.profile_url,
            {
                "first_name":"test",
                "address":"ktm"
            },
            format='multipart'
        )

        self.assertEqual(res.status_code, 429)
        self.assertIn("detail", res.data)