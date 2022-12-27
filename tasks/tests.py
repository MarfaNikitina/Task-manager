from django.contrib.messages import get_messages
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
        cls.task2 = Task.objects.get(pk=2)
        cls.user = User.objects.get(pk=2)
        cls.tasks_url = reverse('tasks')

    def assertTask(self, task, task_data):
        self.assertEqual(task.__str__(), task_data['name'])
        self.assertEqual(task.name, task_data['name'])

    def test_task_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tasks_url)
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
        new_task_data = self.test_data["tasks"]["new"]
        response = self.client.post(reverse('create_task'), new_task_data)
        created_task = Task.objects.get(name=new_task_data['name'])
        self.assertRedirects(response, self.tasks_url)
        self.assertTask(created_task, new_task_data)

    def test_update_task_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('update_task', args=(self.task.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        self.client.force_login(self.user)
        new_task_data = self.test_data["tasks"]["new"]
        response = self.client.post(reverse(
            'update_task', args=[self.task.pk]), new_task_data
        )
        self.assertRedirects(response, self.tasks_url)
        updated_task = Task.objects.get(name=new_task_data['name'])
        self.assertTask(updated_task, new_task_data)

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('delete_task', args=(self.task.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_task', args=(self.task.pk,))
        )
        self.assertRedirects(response, self.tasks_url)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name=self.task.name)

    def test_delete_no_permission(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_task', args=(self.task2.pk,))
        )
        self.assertRedirects(response, self.tasks_url)
        assert self.task2 in Task.objects.all()
        self.assertEqual(1, len(list(get_messages(response.wsgi_request))))
