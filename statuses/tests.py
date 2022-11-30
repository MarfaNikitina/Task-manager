from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from task_manager.utils import get_test_data, get_fixture_data


# class StatusTest(TestCase):
#     fixtures = ['statuses.json']
# 
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_data = get_test_data()
# 
#     def assertStatus(self, status, status_data):
#         self.assertEqual(status.__str__(), status_data['name'])
#         self.assertEqual(status.name, status_data['name'])
# 
#     def test_status_page(self):
#         response = self.client.get(reverse('statuses'))
#         self.assertEqual(response.status_code, 200)
# 
#         statuses = Status.objects.all()
#         self.assertQuerysetEqual(
#             response.context['status_list'],
#             statuses,
#             ordered=False,
#         )
# 
#     def test_status_create_page(self):
#         response = self.client.get(reverse('create_status'))
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_status(self):
#         new_status_data = self.test_data['statuses']['new']
#         response = self.client.post(reverse('create_status'), new_status_data)
# 
#         self.assertRedirects(response, reverse('statuses'))
#         created_status = Status.objects.get(name=new_status_data['name'])
#         self.assertStatus(created_status, new_status_data)
# 
#     def test_update_status_page(self):
#         exist_status_data = self.test_data['statuses']['existing']
#         exist_status = Status.objects.get(name=exist_status_data['name'])
#         response = self.client.get(reverse('update_status', args=[exist_status.pk]))
# 
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_status(self):
#         exist_status_data = self.test_data['statuses']['existing']
#         new_status_data = self.test_data['statuses']['new']
#         exist_status = Status.objects.get(name=exist_status_data['name'])
#         response = self.client.post(
#             reverse('update_status', args=[exist_status.pk]),
#             new_status_data,
#         )
# 
#         self.assertRedirects(response, reverse('statuses'))
#         updated_status = Status.objects.get(name=new_status_data['name'])
#         self.assertStatus(updated_status, new_status_data)



# class StatusTest(TestCase):
#     fixtures = ['statuses.json']
# 
#     def setUp(self):
#         self.status1 = Status.objects.get(pk=1)
#         self.status2 = Status.objects.get(pk=2)
#         self.users_list = reverse('statuses')
#         self.form_data = {'name': 'in process'}
# 
#     def test_statuses_view(self):
#         response = self.client.get(reverse('statuses'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Warning')
#         self.assertContains(response, 'New')
# 
#     def test_status_create(self):
#         response = self.client.get(reverse('create_status'))
#         self.assertEqual(response.status_code, 200)
#         response_post = self.client.post(reverse('create_status'), self.form_data)
#         self.assertRedirects(response_post, self.users_list)
#         self.assertTrue(Status.objects.get(id=3))
# 
#     def test_status_update(self):
#         update_url = reverse('update_status', args=(self.status1.id,))
#         response = self.client.get(update_url)
#         self.assertEqual(response.status_code, 200)
#         response_post = self.client.post(update_url, self.form_data)
#         self.assertRedirects(response_post, self.users_list)
#         status = Status.objects.get(pk=1)
#         self.assertEqual(status.name, self.form_data['name'])
# 
#     def test_delete_status(self):
#         delete_url = reverse('delete_status', args=(self.status1.id,))
#         response = self.client.get(delete_url)
#         self.assertEqual(response.status_code, 200)
#         response_post = self.client.post(delete_url)
#         self.assertRedirects(response_post, self.users_list)
#         with self.assertRaises(ObjectDoesNotExist):
#             Status.objects.get(id=self.status1.id)

