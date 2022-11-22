from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.utils import get_test_data


class CreateUserTests(TestCase):

    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def assertUser(self, user, user_data):
        self.assertEqual(user.__str__(), user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_create_page(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_user_data = self.test_data['users']['new']
        response = self.client.post(reverse('users:create'), new_user_data)

        self.assertRedirects(response, reverse('users:users'))
        created_user = User.objects.get(name=new_user_data['username'])
        self.assertUser(created_user, new_user_data)


# class CategoriesTest(TestCase):
#     def setUp(self):
#         category1 = {
#                 'id': 1,
#                 'name': 'English Authors',
#                 'description': 'Classic literature'
#             }
#         self.category1 = Category(**category1)
#         category2 = {
#                 'id': 2,
#                 'name': 'Russian Authors',
#                 'description': 'Modern literature'
#             }
#         self.category2 = Category(**category2)
#         self.categories = Category.objects.bulk_create(
#             [self.category1, self.category2]
#         )
# 
#     def test_category_view(self):
#         response = self.client.get('/categories/')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'English Authors')
#         self.assertContains(response, 'Classic literature')
#         self.assertContains(response, 'Russian Authors')
#         self.assertContains(response, 'Modern literature')
