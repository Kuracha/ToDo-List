from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('DONE', 'Done'),
    )
    name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='NEW')
    date = models.DateField(verbose_name='completion date')
    description = models.TextField()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f'Task {self.name} created by {self.user}'
