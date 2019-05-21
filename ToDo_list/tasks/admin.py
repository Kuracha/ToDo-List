from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'status', 'completion_date', 'description',)
    list_filter = ('status',)
    date_hierarchy = 'completion_date'


admin.site.register(Task, TaskAdmin)
