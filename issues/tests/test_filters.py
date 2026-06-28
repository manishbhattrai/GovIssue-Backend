from issues.tests.test_setup import TestSetup


class TestIssueFilters(TestSetup):

    def test_filter_by_category_slug(self):

        self.authenticate(self.user)

        category = self.categories[0]

        res = self.client.get(
            self.create_list_issue_url,
            {
                "category":category.slug
            }
        )

        self.assertEqual(res.status_code, 200)

        results = res.data['results']
        for issue in results:
            self.assertEqual(issue["category"]["name"], category.name)
