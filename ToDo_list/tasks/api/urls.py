from django.urls import path, include

from rest_framework import routers

from .views import TaskViewset, TaskIndexAPIView, TaskDetailAPIView, UserTasksAPIView, TaskUpdateStatusAPIView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewset),

urlpatterns = [
    path('', include(router.urls)),
    path('index/', TaskIndexAPIView.as_view(), name='index'),
    path('index/<pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('index/<pk>/edit', TaskUpdateStatusAPIView.as_view(), name='edit_status'),
    path('my_tasks/', UserTasksAPIView.as_view(), name='my_tasks'),
]