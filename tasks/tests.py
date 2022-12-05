from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task
from task_manager.utils import get_test_data
from users.models import User


class TaskTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()
        cls.task = Task.objects.get(pk=1)
        cls.user = User.objects.get(pk=1)

    def assertTask(self, task, task_data):
        self.assertEqual(task.__str__(), task_data['name'])
        self.assertEqual(task.name, task_data['name'])

    def test_task_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertQuerysetEqual(
            response.context['task_list'],
            tasks,
            ordered=False,
        )

    def test_task_create_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        self.client.force_login(self.user)
        new_task_data = self.test_data['tasks']['new']
        response = self.client.post(reverse('create_task'), new_task_data)

        self.assertRedirects(response, reverse('tasks'))
        created_task = Task.objects.get(name=new_task_data['name'])
        self.assertTask(created_task, new_task_data)

    def test_update_task_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('update_task', args=(self.task.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        self.client.force_login(self.user)
        new_task_data = self.test_data['tasks']['new']
        response = self.client.post(
            reverse('update_task', args=[self.task.pk]),
            new_task_data,
        )

        self.assertRedirects(response, reverse('statuses'))
        updated_task = Task.objects.get(name=new_task_data['name'])
        self.assertStatus(updated_task, new_task_data)

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('delete_task', args=(self.user.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_task', args=(self.user.pk, ))
        )
        self.assertRedirects(response, reverse('tasks'))
        # with self.assertRaises(ObjectDoesNotExist):
        #     Task.objects.get(name=self.task.name)
