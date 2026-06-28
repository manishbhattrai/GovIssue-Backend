from issues.tests.test_setup import TestSetup


class TestPagination(TestSetup):

    def test_pagination_structure(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.create_list_issue_url,
        )

        self.assertEqual(res.status_code, 200)

        self.assertIn("next", res.data)
        self.assertIn("previous", res.data)
        self.assertIn("results", res.data)
