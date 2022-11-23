from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from .models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()
from task_manager.utils import get_test_data, get_fixture_data


class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.users_list = reverse('users')
        self.login = reverse('login')
        self.form_data = {'username': 'Woddie',
                          'first_name': 'Woddie',
                          'last_name': 'Allen',
                          'password': '1570127',
                          'password2': '1570127'}

    def test_user_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mike')
        self.assertContains(response, 'Marfa')

    def test_user_create(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(reverse('create'), self.form_data)
        self.assertRedirects(response_post, self.login)
        self.assertTrue(User.objects.get(id=3))

    def test_user_update(self):
        update_url = reverse('update', args=(self.user1.id,))
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(update_url, self.form_data)
        self.assertRedirects(response_post, reverse('users'))
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, self.form_data['username'])

    def test_delete_user(self):
        delete_url = reverse('delete', args=(self.user1.id,))
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(delete_url)
        self.assertRedirects(response_post, reverse('users'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.user1.id)

    # def setUp(self):
    #     user1 = {
    #             'id': 1,
    #             'username': 'MikeZh',
    #             'first_name': 'Mike',
    #             'password': '1570127'
    #         }
    #     self.user1 = User(**user1)
    #     user2 = {
    #             'id': 2,
    #             'username': 'MarfaN',
    #             'first_name': 'Marfa',
    #             'password': '1234567'
    #         }
    #     self.user2 = User(**user2)
    #     self.users = User.objects.bulk_create(
    #         [self.user1, self.user2]
    #     )
    #     self.users_list = reverse('users')
    #     self.login = reverse('login')
    #     self.form_data = {'username': 'Woddie',
    #                       'first_name': 'Woddie',
    #                       'last_name': 'Allen',
    #                       'password': '1570127',
    #                       'password2': '1570127'}