from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'date', 'description',)
    list_filter = ('status',)
    date_hierarchy = 'date'


admin.site.register(Task, TaskAdmin)
