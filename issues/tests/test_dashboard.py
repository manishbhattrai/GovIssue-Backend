from issues.tests.test_setup import TestSetup


class TestDashboard(TestSetup):


    def test_user_dashboard(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.dashboard_url
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["chart_type"], "bar")

    def test_admin_dashboard(self):

        self.authenticate(self.admin)

        res = self.client.get(
            self.dashboard_url
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["chart_type"], "pie")