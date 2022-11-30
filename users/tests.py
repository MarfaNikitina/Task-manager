from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from .models import User
# from django.contrib.auth import get_user_model
from task_manager.utils import get_test_data, get_fixture_data


class UserTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()
        cls.user = User.objects.get(pk=1)

    def assertUser(self, user, user_data):
        # self.assertEqual(user.__str__(), user_data['name'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_user_list(self):
        response = self.client.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        self.assertQuerysetEqual(
            response.context['user_list'],
            users,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_user_data = self.test_data['users']['new']
        response = self.client.post(reverse('users:create'), new_user_data)
        created_user = User.objects.get(first_name=new_user_data['first_name'])
        self.assertRedirects(response, reverse('login'))

        self.assertUser(created_user, new_user_data)

    def test_update_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:update', args=[self.user.pk]),
            self.test_data['users']['new'],
        )
        self.assertRedirects(response, reverse('users:users'))
        updated_user = User.objects.get(first_name=self.test_data['users']['new']['first_name'])
        self.assertUser(updated_user, self.test_data['users']['new'])

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:delete', args=[self.user.pk]))
        self.assertRedirects(response, reverse('users:users'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.user['username'])


# class UserTests(TestCase):
#     fixtures = ['users.json']
# 
#     def setUp(self):
#         self.user1 = User.objects.get(pk=1)
#         self.user2 = User.objects.get(pk=2)
#         self.users_list = reverse('users')
#         self.login = reverse('login')
#         self.form_data = {'username': 'Woddie',
#                           'first_name': 'Woddie',
#                           'last_name': 'Allen',
#                           'password': '1570127',
#                           'password2': '1570127'}
# 
#     def test_user_view(self):
#         response = self.client.get(reverse('users'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Mike')
#         self.assertContains(response, 'Marfa')
# 
#     def test_user_create(self):
#         self.client.force_login(self.user1)
#         User.objects.create(self.form_data)
#         response_post = self.client.post(reverse('create'), self.form_data)
#         self.assertRedirects(response_post, self.login)
#         self.assertTrue(User.objects.get(id=3))
#         self.assertContains(response, 'Mike')
# 
#     def test_user_update(self):
#         self.client.force_login(self.user1)
#         update_url = reverse('update', args=(self.user2.id,))
#         params = {
#             'username': 'a',
#             'first_name': 'lala',
#             'last_name': 'OOps',
#         }
#         response = self.client.post(
#             update_url,
#             data=params,
#         )
#         self.assertEqual(response.status_code, 302)
#         created_user = User.objects.get(username='a')
#         self.assertEqual(created_user.username, params['username'])
# 
#         update_url = reverse('update', args=(self.user1.id,))
#         response = self.client.get(update_url)
#         self.assertEqual(response.status_code, 200)
#         response_post = self.client.post(update_url, self.form_data)
#         self.assertRedirects(response_post, reverse('login'))
#         user = User.objects.get(pk=1)
#         self.assertEqual(user.username, self.form_data['username'])
# 
#     def test_delete_user(self):
#         self.client.force_login(self.user1)
#         delete_url = reverse('delete', args=(self.user2.id,))
#         response = self.client.get(delete_url)
#         self.assertEqual(response.status_code, 200)
#         response_post = self.client.post(delete_url)
#         self.assertRedirects(response_post, reverse('users'))
#         with self.assertRaises(ObjectDoesNotExist):
#             User.objects.get(id=self.user2.id)
