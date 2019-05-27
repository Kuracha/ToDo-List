from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from datetime import date

from ..models import Task


class TaskIndexAPI(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='TestUser',
            password='test1234'
        )
        Task.objects.create(
            name='Task for test',
            creator=user,
            completion_date=date(2019, 4, 19),
            description='This is description for test purposes',
        )

    def test_access(self):
        response = self.client.get(reverse('tasks_index'), format='json')
        self.assertEqual(response.status_code, 200,  f'expected Response code 200, instead get {response.status_code}')

    def test_check_if_delayed(self):
        response = self.client.get(reverse('tasks_index'), format='json')
        self.assertIn(('warning_if_delayed', 'This task is delayed'), response.data)


class TaskDetailAPI(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='TestUser',
            password='test1234'
        )
        Task.objects.create(
            name='Task for test',
            creator=user,
            status='Unauthenticated',
            completion_date=date(2019, 4, 9),
            description='This is description for test purposes',
            warning_if_delayed=''
        )

    def test_access(self):
        task = Task.objects.get(id=1)
        response = self.client.get(reverse('task_detail', kwargs={'pk': task.id}), format='json')
        self.assertEqual(response.status_code, 200,  f'expected Response code 200, instead get {response.status_code}')


class TaskUpdateStatusAPI(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='test',
            password='test123'
        )
        user2 = User.objects.create_user(
            username='test2',
            password='test123'
        )
        client = APIClient()
        client.force_authenticate(user=user2)
        Task.objects.create(
            name='Task for test',
            creator=User.objects.get(username='test2'),
            status='Unauthenticated',
            completion_date=date(2019, 4, 9),
            description='This is description for test purposes',
            warning_if_delayed=''
        )

    def test_access_unauthenticated_user(self):
        task = Task.objects.get(id=1)
        data = {"status": "DONE"}
        response = self.client.post(reverse('edit_task_status', kwargs={'pk': task.id}), data, format='json')
        self.assertEqual(response.status_code, 405, f'expected Response code 405, instead get {response.status_code}')

    def test_access_authenticated_user_without_permission(self):
        task = Task.objects.get(id=1)
        login = self.client.login(username='test', password='test123')
        data = {"status": "DONE"}
        response = self.client.post(reverse('edit_task_status', kwargs={'pk': task.id}), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 405, f'expected Response code 405, instead get {response.status_code}')


class UserTasksAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user1 = User.objects.create_user(
            username='test',
            password='test123'
        )
        user2 = User.objects.create_user(
            username='test2',
            password='test123'
        )
        Task.objects.create(
            name=f'Task for test',
            creator=user1,
            status='Unauthenticated',
            completion_date=date(2023, 8, 10),
            description='This is description for test purposes',
            warning_if_delayed=''
        )
        Task.objects.create(
            name=f'Task for test4',
            creator=user2,
            status='Unauthenticated',
            completion_date=date(2019, 4, 10),
            description='This is description for test purposes',
            warning_if_delayed=''
        )

    def test_access_unauthenticated_user(self):
        Task.objects.all()
        login = self.client.login()
        response = self.client.get(reverse('user_tasks'))
        self.assertFalse(login)
        self.assertEqual(response.status_code, 403, f'expected Response code 403, instead get {response.status_code}')

    def test_access_authenticated_user(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        response = self.client.get(reverse('user_tasks'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200, f'expected Response code 200, instead get {response.status_code}')

    def test_post_authenticated_user_valid(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        data = {
            "name": "Testing Task",
            "completion_date": "2019-04-19",
            "description": "Testing task description belonging to Test creator"
        }
        response = self.client.post(reverse('user_tasks'), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 201, f'expected Response code 201, instead get {response.status_code}')

    def test_post_authenticated_user_invalid(self):
        Task.objects.all()
        login = self.client.login(username='test2', password='test123')
        data = {
            "name": "Testing Task",
            "completion_date": 2019-4-19,
            "description": "Testing task description belonging to Test creator"
        }
        response = self.client.post(reverse('user_tasks'), data, format='json')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 400, f'expected Response code 400, instead get {response.status_code}')
