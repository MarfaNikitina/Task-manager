from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from task_manager.utils import get_test_data, get_fixture_data
from users.models import User


class StatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()
        cls.status = Status.objects.get(pk=1)
        cls.user = User.objects.get(pk=1)

    def assertStatus(self, status, status_data):
        self.assertEqual(status.__str__(), status_data['name'])
        self.assertEqual(status.name, status_data['name'])

    def test_status_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

        statuses = Status.objects.all()
        self.assertQuerysetEqual(
            response.context['status_list'],
            statuses,
            ordered=False,
        )

    def test_status_create_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        self.client.force_login(self.user)
        new_status_data = self.test_data['statuses']['new']
        response = self.client.post(reverse('create_status'), new_status_data)

        self.assertRedirects(response, reverse('statuses'))
        created_status = Status.objects.get(name=new_status_data['name'])
        self.assertStatus(created_status, new_status_data)

    def test_update_status_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('update_status', args=(self.status.pk, )))
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        self.client.force_login(self.user)
        new_status_data = self.test_data['statuses']['new']
        response = self.client.post(
            reverse('update_status', args=[self.status.pk]),
            new_status_data,
        )

        self.assertRedirects(response, reverse('statuses'))
        updated_status = Status.objects.get(name=new_status_data['name'])
        self.assertStatus(updated_status, new_status_data)

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_status', args=(self.user.pk, )))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_status', args=(self.user.pk, )))
        self.assertRedirects(response, reverse('statuses'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name=self.status.name)
