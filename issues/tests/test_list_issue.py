from .test_setup import TestSetup


class TestListIssue(TestSetup):


    def test_list_excludes_own_and_pending(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.create_list_issue_url
        )
        self.assertEqual(res.status_code, 200)

        results = res.data["results"]
        for result in results:
            self.assertEqual(len(results), 5)
            self.assertNotIn("p", result['status'])

    def test_admin_can_see_all_issues(self):

        self.authenticate(self.admin)
        res = self.client.get(
            self.create_list_issue_url
        )
        self.assertEqual(res.status_code, 200)

        results = res.data['results']
        self.assertEqual(len(results), 5)