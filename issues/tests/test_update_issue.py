from issues.tests.test_setup import TestSetup
from django.urls import reverse


class TestUpdateIssue(TestSetup):

    def test_owner_can_update(self):

        self.authenticate(self.user)
        issue = self.issues[0]
        url = reverse("issue-detail", kwargs={"issue_id": issue.issue_id})

        res = self.client.patch(
            url,
            {
                "title": "Updated Title"
            }
        )

        self.assertEqual(res.status_code, 200)
        issue.refresh_from_db()
        self.assertEqual(issue.title, "Updated Title")

    def test_non_owner_forbidden(self):

        self.authenticate(self.user2)
        issue = self.issues[0]
        url = reverse("issue-detail", kwargs={"issue_id": issue.issue_id})

        res = self.client.patch(
            url,
            {
                "title": "Hack Attempt"
            }
        )


        self.assertEqual(res.status_code, 403)