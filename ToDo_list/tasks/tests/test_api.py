from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from datetime import date

from ..models import Task


class TaskIndexAPI(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='TestUser', password='test1234')
        Task.objects.create(name='Task for test', user=user, status='New', date=date(2019, 4, 9),
                            description='This is description for test purposes', delayed='This task is delayed')

    def test_access(self):
        Task.objects.all()
        response = self.client.get(reverse('index'), format='json')
        self.assertEqual(response.status_code, 200,  f'expected Response code 200, instead get {response.status_code}')


class TaskDetailAPI(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='TestUser', password='test1234')
        Task.objects.create(name='Task for test', user=user, status='New', date=date(2019, 4, 9),
                            description='This is description for test purposes', delayed='This task is delayed')

    def test_access(self):
        task = Task.objects.get(id=1)
        response = self.client.get(reverse('task_detail', kwargs={'pk': task.id}), format='json')
        self.assertEqual(response.status_code, 200,  f'expected Response code 200, instead get {response.status_code}')


class TaskUpdateStatusAPI(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test123')
        user2 = User.objects.create_user(username='test2', password='test123')
        client = APIClient()
        client.force_authenticate(user=user2)
        Task.objects.create(name='Task for test', user=User.objects.get(username='test2'), status='New',
                            date=date(2019, 4, 9), description='This is description for test purposes')

    def test_access_unauthenticated_user(self):
        task = Task.objects.get(id=1)
        data = {"status": "DONE"}
        response = self.client.post(reverse('edit_status', kwargs={'pk': task.id}), data, format='json')
        self.assertEqual(response.status_code, 405, f'expected Response code 405, instead get {response.status_code}')

    def test_access_authenticated_user_without_permission(self):
        task = Task.objects.get(id=1)
        login = self.client.login(username='test', password='test123')
        data = {"status": "DONE"}
        response = self.client.post(reverse('edit_status', kwargs={'pk': task.id}), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 405, f'expected Response code 405, instead get {response.status_code}')


class MyTasksAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user1 = User.objects.create_user(username='test', password='test123')
        user2 = User.objects.create_user(username='test2', password='test123')
        Task.objects.create(name=f'Task for test', user=user1, status='New', date=date(2019, 4, 9),
                            description='This is description for test purposes')
        Task.objects.create(name=f'Task for test4', user=user2, status='New', date=date(2019, 4, 10),
                            description='This is description for test purposes')

    def test_access_unauthenticated_user(self):
        Task.objects.all()
        login = self.client.login()
        response = self.client.get(reverse('my_tasks'))
        self.assertFalse(login)
        self.assertEqual(response.status_code, 403, f'expected Response code 403, instead get {response.status_code}')

    def test_access_authenticated_user(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        response = self.client.get(reverse('my_tasks'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200, f'expected Response code 200, instead get {response.status_code}')

    def test_post_authenticated_user_valid(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        data = {
            "name": "Testing Task",
            "date": "2019-04-19",
            "description": "Testing task description belonging to Test user"
        }
        response = self.client.post(reverse('my_tasks'), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 201, f'expected Response code 201, instead get {response.status_code}')

    def test_post_authenticated_user_invalid(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        data = {
            "name": "Testing Task",
            "date": 2019-4-19,
            "description": "Testing task description belonging to Test user"
        }
        response = self.client.post(reverse('my_tasks'), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 400, f'expected Response code 400, instead get {response.status_code}')
