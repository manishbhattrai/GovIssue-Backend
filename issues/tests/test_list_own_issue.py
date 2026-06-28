from issues.tests.test_setup import TestSetup


class TestListOwnIssue(TestSetup):

    def test_only_own_issues_returned(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.own_issue_list_url
        )

        self.assertEqual(res.status_code, 200)

        results = res.data['results']
        for issue in results:
            self.assertEqual(issue["created_by"]["full_name"], self.user.full_name)
