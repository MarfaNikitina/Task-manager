from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.utils import get_test_data, get_fixture_data


class UserTests(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def setUp(self):
        user1 = {
                'id': 1,
                'username': 'MikeZh',
                'first_name': 'Mike',
                'password': '1570127'
            }
        self.user1 = User(**user1)
        user2 = {
                'id': 2,
                'username': 'MarfaN',
                'first_name': 'Marfa',
                'password': '1234567'
            }
        self.user2 = User(**user2)
        self.users = User.objects.bulk_create(
            [self.user1, self.user2]
        )
        self.users_list = reverse('users')
        self.login = reverse('login')
        self.form_data = {'username': 'Woddie',
                          'first_name': 'Woddie',
                          'last_name': 'Allen',
                          'password': '1570127',
                          'password2': '1570127'}

    def test_users_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MikeZh')
        self.assertContains(response, 'MarfaN')

    def test_user_create(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(reverse('create'), self.form_data)
        self.assertRedirects(response_post, self.login)
        self.assertTrue(User.objects.get(id=3))


