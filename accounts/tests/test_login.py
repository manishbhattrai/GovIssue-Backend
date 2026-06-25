from .test_setup import TestSetup

class LoginTest(TestSetup):

    def test_valid_login(self):

        res = self.client.post(
            self.login_url,
            {
                "email":"test.user@gmail.com",
                "password":"TestPassword123!"
            },
            format='json'
        )

        access_token = res.data['token']
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.data)
        self.assertIsNotNone("token", access_token)

    def test_login_empty_field(self):

        payload = {
            "email": "",
            "password": ""
        }

        res = self.client.post(
            self.login_url,
            payload,
            format="json"
        )

        self.assertEqual(res.status_code, 400)

    def test_login_empty_password(self):

        payload = {
            "email": "test.user@gmail.com",
            "password": ""
        }

        res = self.client.post(
            self.login_url,
            payload,
            format="json"
        )

        self.assertEqual(res.status_code, 400)

    def test_invalid_password_login(self):

        res = self.client.post(
            self.login_url,
            {
                "email":"test.user@gmail.com",
                "password":"wrongpassword"
            },
            format='json'
        )

        self.assertEqual(res.status_code, 401)

    def test_invalid_email_login(self):

        res = self.client.post(
            self.login_url,
            {
                "email": "wronguser@gmail.com",
                "password": "TestPassword123!"
            },
            format='json'
        )

        self.assertEqual(res.status_code, 401)

    def test_nonexistent_user_login(self):

        res = self.client.post(
            self.login_url,
            {
                "email": "wronguser@gmail.com",
                "password": "wrong1234!"
            },
            format='json'
        )

        self.assertEqual(res.status_code, 401)
