from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from task_manager.utils import get_test_data, get_fixture_data


class UserTests(TestCase):

    def setUp(self):
        self.status1 = Status.objects.create(
            id=1,
            name='Warning'
        )
        self.status2 = Status.objects.create(
            id=2,
            name='New'
        )
        self.users_list = reverse('statuses')
        self.form_data = {'name': 'in process'}

    def test_statuses_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Warning')
        self.assertContains(response, 'New')

    def test_status_create(self):
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(reverse('create_status'), self.form_data)
        self.assertRedirects(response_post, self.users_list)
        self.assertTrue(Status.objects.get(id=3))

    def test_status_update(self):
        update_url = reverse('update_status', args=(self.status1.id,))
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(update_url, self.form_data)
        self.assertRedirects(response_post, self.users_list)
        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, self.form_data['name'])

    def test_delete_status(self):
        delete_url = reverse('delete_status', args=(self.status1.id,))
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(delete_url)
        self.assertRedirects(response_post, self.users_list)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=self.status1.id)

