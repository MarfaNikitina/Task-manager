from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from .models import User
# from django.contrib.auth import get_user_model
from task_manager.utils import get_test_data


class UserTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client = Client()

        self.user = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.users_list = reverse('users:users')
        self.test_data = get_test_data()
        self.login = reverse('login')

    def test_user_exists(self):
        self.assertTrue(User.objects.count() == 3)

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

    # def test_create(self):
    #     new_user_data = self.test_data['users']['new']
    #     # cnew_user_data.pop('username')
    #     # new_user_data = ''
    #     print('####', new_user_data)
    #     response = self.client.post('/users/create', new_user_data, follow=True)
    #     print(response.status_code, response)
    #     u = User.objects.all()
    #     print(u)
    #     created_user = User.objects.get(username=new_user_data['username'])
    #     self.assertRedirects(response, reverse('login'))
    #     self.assertRedirects(response, reverse('login'))
    #     self.assertUser(created_user, new_user_data)

    def test_update_page(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse('users:update', args=(self.user2.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    # def test_update(self):
    #     self.client.force_login(self.user)
    #     response = self.client.post(
    #         reverse('users:update', args=[self.user.pk, ]),
    #         self.test_data['users']['new'],
    #     )
    #     self.assertRedirects(response, reverse('users:users'))
    #     # # self.assertEqual(response.status_code, 200)
    #     updated_user = User.objects.get(
    #         first_name=self.test_data['users']['new']['first_name']
    #     )
    #     # updated_user = User.objects.get(first_name='Marfa')
    #     self.assertUser(updated_user, self.test_data['users']['new'])

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('users:delete', args=(self.user.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:delete', args=(self.user.pk, ))
        )
        self.assertRedirects(response, reverse('users:users'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.user.username)
