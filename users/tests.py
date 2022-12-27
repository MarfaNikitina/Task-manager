from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from task_manager.utils import get_test_data
from task_manager.messages import USER_EXIST_MESSAGE, VALIDATION_ERROR_MESSAGE


class UserTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.client = Client()

        self.user = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.users_url = reverse('users:users')
        self.test_data = get_test_data()
        self.login_url = reverse('login')

    def test_user_exists(self):
        self.assertTrue(User.objects.count() == 3)

    def assertUser(self, user, user_data):
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_user_list(self):
        response = self.client.get(self.users_url)
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

    def test_create_user(self):
        create_user = reverse('users:create')
        new_user_data = self.test_data["users"]["new"]
        post_response = self.client.post(create_user,
                                         new_user_data, follow=True)
        self.assertRedirects(post_response, self.login_url)
        self.assertTrue(User.objects.get(username=new_user_data['username']))

    def test_create_exist_user(self):
        create_user = reverse('users:create')
        new_user_data = self.test_data["users"]["already_exist"]
        post_response = self.client.post(create_user,
                                         new_user_data, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(
            post_response, text=USER_EXIST_MESSAGE)

    def test_create_wrong_user(self):
        create_user = reverse('users:create')
        wrong_user_data = self.test_data["users"]["wrong_user"]
        post_response = self.client.post(create_user,
                                         wrong_user_data, follow=True)
        errors = post_response.context['form'].errors
        self.assertIn('last_name', errors)
        self.assertEqual(
            [VALIDATION_ERROR_MESSAGE],
            errors['last_name']
        )
        self.assertRaises(ValidationError)
        wrong2_user_data = self.test_data["users"]["wrong_user2"]
        post_response2 = self.client.post(create_user,
                                          wrong2_user_data, follow=True)
        errors = post_response2.context['form'].errors
        self.assertIn('first_name', errors)
        self.assertEqual(
            [VALIDATION_ERROR_MESSAGE],
            errors['first_name']
        )
        self.assertRaises(ValidationError)

    def test_update_page(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse('users:update', args=(self.user2.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_no_permission(self):
        self.client.force_login(self.user2)
        response_no_permission = self.client.get(
            reverse('users:update', args=(self.user.pk, ))
        )
        self.assertRedirects(response_no_permission, self.users_url)
        self.assertEqual(1, len(list(
            get_messages(response_no_permission.wsgi_request))))

    def test_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:update', args=(self.user.pk, )),
            self.test_data["users"]["new"]
        )
        self.assertRedirects(response, self.users_url)
        updated_user = User.objects.get(
            first_name=self.test_data["users"]["new"]['first_name']
        )
        self.assertUser(updated_user, self.test_data["users"]["new"])

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('users:delete', args=(self.user.pk, ))
        )
        self.assertEqual(response.status_code, 200)
        response_no_permission = self.client.get(
            reverse('users:delete', args=(self.user2.pk,))
        )
        self.assertRedirects(response_no_permission, self.users_url)
        self.assertEqual(1, len(list(
            get_messages(response_no_permission.wsgi_request))))

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:delete', args=(self.user.pk, ))
        )
        self.assertRedirects(response, self.users_url)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.user.username)
