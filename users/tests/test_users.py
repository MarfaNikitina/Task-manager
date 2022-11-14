from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class CreateUserTests(TestCase):

    def setUp(self):
        # Создание двух пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()





# class YourTestClass(TestCase):
# 
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass
# 
#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass
# 
#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)
# 
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)
# 
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)