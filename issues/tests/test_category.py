from .test_setup import TestSetup
from django.urls import reverse


class CategoryTest(TestSetup):

    def test_category_create_success(self):

        self.authenticate(self.admin)
        payload = {
            "name": "Electronics",
            "description": "testing category"
        }

        res = self.client.post(
            self.create_list_category_url,
            payload,
            format='json'
        )
        self.assertEqual(res.status_code, 201)


    def test_category_cannot_be_created_by_user(self):

        self.authenticate(self.user)

        payload = {
            "name":"Electronics",
            "description":"testing category"
        }
        res = self.client.post(
            self.create_list_category_url,
            payload,
            format='json'
        )

        self.assertEqual(res.status_code,403)

    def test_category_can_be_access_by_user(self):

        self.authenticate(self.user)

        res = self.client.get(
            self.create_list_category_url
        )

        self.assertEqual(res.status_code,200)

        for item in res.data:
            self.assertIn("name", item)

        self.assertEqual(len(res.data),5)


    def test_category_cannot_be_accessed_by_unauthenticated_user(self):

        res = self.client.get(
            self.create_list_category_url
        )

        self.assertEqual(res.status_code, 401)

    def test_category_update_success(self):

        self.authenticate(self.admin)

        category = self.categories[1]
        url = reverse('category-detail', kwargs={'slug': category.slug})

        payload = {
            "name":"updated electronics",
            "description":"Test"
        }

        res = self.client.patch(
            url,
            payload,
            format='json'
        )
        self.assertEqual(res.status_code,200)

        category.refresh_from_db()
        self.assertEqual(category.name, "updated electronics")

    def test_category_cannot_be_modified_by_user(self):

        self.authenticate(self.user)

        category = self.categories[1]
        url = reverse('category-detail', kwargs={'slug': category.slug})
        payload = {
            "name": "updated_electronics",
            "description": "Test"
        }

        res = self.client.patch(
            url,
            payload,
            format='json'
        )
        self.assertEqual(res.status_code, 403)

    def test_category_delete_success(self):

        self.authenticate(self.admin)

        category = self.categories[1]
        url = reverse('category-detail', kwargs={'slug': category.slug})
        res = self.client.delete(
            url
        )
        self.assertEqual(res.status_code,204)

    def test_category_cannot_be_deleted_by_user(self):

        self.authenticate(self.user)

        category = self.categories[0]
        url = reverse('category-detail', kwargs={'slug': category.slug})
        res = self.client.delete(
            url
        )
        self.assertEqual(res.status_code,403)