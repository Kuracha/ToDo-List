from django.urls import path, include

from rest_framework import routers

from .views import \
    TasksViewset, \
    TasksIndexAPIView, \
    TaskDetailAPIView, \
    UserTasksAPIView, \
    TaskUpdateStatusAPIView

router = routers.DefaultRouter()
router.register(r'tasks', TasksViewset),

urlpatterns = [
    path('', include(router.urls)),
    path('index/', TasksIndexAPIView.as_view(), name='tasks_index'),
    path('index/<pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('my_tasks/<pk>', TaskUpdateStatusAPIView.as_view(), name='edit_task_status'),
    path('my_tasks/', UserTasksAPIView.as_view(), name='user_tasks'),
]