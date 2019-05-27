from django.http import Http404

from datetime import date

from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models import Task
from .serializer import \
    TaskDetailSerializer, \
    TasksIndexSerializer, \
    UserTasksSerializer, \
    UpdateTaskStatusSerializer, \
    CreateTaskSerializer
from .permission import IsOwnerOrReadOnly


class TasksViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TasksIndexAPIView(APIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'creator__username')

    def get_queryset(self):
        return Task.objects.all()

    def filter_queryset(self, queryset):
        for obj in list(self.filter_backends):
            queryset = obj().filter_queryset(self.request, queryset, self)
            return queryset

    def check_if_tasks_are_delayed(self, queryset):
        checked_tasks = queryset
        for task in checked_tasks:
            if task.completion_date <= date.today() and task.status == 'Unfinished':
                task.warning_if_delayed = 'This task is delayed'
                task.save()
            else:
                task.warning_if_delayed = ''
                task.save()
        return checked_tasks

    def get(self, request):
        tasks_filter = self.filter_queryset(self.get_queryset())
        tasks_index = self.check_if_tasks_are_delayed(tasks_filter)
        pagination_class = PageNumberPagination()
        page = pagination_class.paginate_queryset(tasks_index, request)
        serializer = TasksIndexSerializer(page, many=True)
        return pagination_class.get_paginated_response(serializer.data)


class TaskDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def check_if_task_is_delayed(self, task):
        checked_task = task
        if checked_task.completion_date <= date.today() and checked_task.status == 'Unfinished':
            checked_task.warning_if_delayed = 'This task is delayed'
            checked_task.save()
        else:
            checked_task.warning_if_delayed = ''
            checked_task.save()
        return checked_task

    def get(self, request, pk):
        obtained_task = self.get_object(pk)
        task = self.check_if_task_is_delayed(obtained_task)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class UserTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)

    def check_if_tasks_are_delayed(self, queryset):
        checked_tasks = queryset
        for task in checked_tasks:
            if task.completion_date <= date.today() and task.status == 'Unfinished':
                task.warning_if_delayed = 'This task is delayed'
                task.save()
            else:
                task.warning_if_delayed = ''
                task.save()
        return checked_tasks

    def get(self, request):
        user_tasks = self.get_queryset()
        tasks = self.check_if_tasks_are_delayed(user_tasks)
        serializer = UserTasksSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateStatusAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskStatusSerializer
    permission_classes = [IsOwnerOrReadOnly]

