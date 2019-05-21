from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = (
        ('Finished', 'Finished'),
        ('Unfinished', 'Unfinished'),
    )
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unfinished')
    completion_date = models.DateField(verbose_name='date for completion')
    warning_if_delayed = models.CharField(max_length=50, default=None, blank=True, verbose_name='warning of delaying')
    description = models.TextField(max_length=500)

    class Meta:
        ordering = ('completion_date',)

    def __str__(self):
        return f'Task {self.name} created by {self.creator}'
