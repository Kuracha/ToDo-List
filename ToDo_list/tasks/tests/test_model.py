from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User

from ..models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser', password='test1234')
        Task.objects.create(name='Task for test', user=user, status='New', date=date(2019, 4, 9),
                            description='This is description for test purposes', delayed='Task is delayed')

    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        field_length = task._meta.get_field('name').max_length
        self.assertEqual(field_length, 50)

    def test_user_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_status_field(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_status_max_length(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('status').max_length
        self.assertEqual(field_label, 4)

    def test_date_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'completion date')

    def test_description_field(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_delayed_field(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('delayed').verbose_name
        self.assertEqual(field_label, 'delayed')

    def test_delayed_max_length(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('delayed').max_length
        self.assertEqual(field_label, 50)
