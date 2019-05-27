from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'status', 'completion_date', 'description',)
    list_filter = ('status',)


admin.site.register(Task, TaskAdmin)
