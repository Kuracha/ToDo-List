from django.urls import path, include

from rest_framework import routers

from .views import TaskViewset, TaskIndexAPIView, TaskDetailAPIView, UserTasksAPIView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewset),

urlpatterns = [
    path('', include(router.urls)),
    path('index/', TaskIndexAPIView.as_view()),
    path('index/<pk>/', TaskDetailAPIView.as_view()),
    path('my_tasks/', UserTasksAPIView.as_view()),
]
