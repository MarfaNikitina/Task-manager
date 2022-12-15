from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from task_manager.utils import get_test_data
from users.models import User


class LabelTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'labels.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()
        cls.label = Label.objects.get(pk=1)
        cls.user = User.objects.get(pk=1)

    def assertLabel(self, label, label_data):
        self.assertEqual(label.__str__(), label_data['name'])
        self.assertEqual(label.name, label_data['name'])

    def test_label_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)

        statuses = Label.objects.all()
        self.assertQuerysetEqual(
            response.context['label_list'],
            statuses,
            ordered=False,
        )

    def test_label_create_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 200)

    def test_create_label(self):
        self.client.force_login(self.user)
        new_label_data = self.test_data['labels']['new']
        response = self.client.post(reverse('create_label'), new_label_data)

        self.assertRedirects(response, reverse('labels'))
        created_status = Label.objects.get(name=new_label_data['name'])
        self.assertLabel(created_status, new_label_data)

    def test_update_label_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            'update_label',
            args=(self.label.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_label(self):
        self.client.force_login(self.user)
        new_label_data = self.test_data['labels']['new']
        response = self.client.post(
            reverse('update_label', args=[self.label.pk]), new_label_data
        )
        self.assertRedirects(response, reverse('labels'))
        updated_status = Label.objects.get(name=new_label_data['name'])
        self.assertLabel(updated_status, new_label_data)

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            'delete_label',
            args=(self.label.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_label(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'delete_label',
            args=(self.label.pk,)), )
        self.assertRedirects(response, reverse('labels'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name=self.label.name)
