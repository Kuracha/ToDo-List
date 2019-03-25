from django.http import Http404
from django.conf import settings
from datetime import date

from rest_framework import viewsets, permissions, generics, filters, status, pagination
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Task
from .serializer import TaskSerializer, IndexSerializer, MyTasksSerializer, StatusSerializer, CreateTaskSerializer
from .permission import IsOwnerOrReadOnly


class TaskViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskIndexAPIView(APIView):

    def filter_queryset(self, queryset):
        for obj in list(self.filter_backends):
            queryset = obj().filter_queryset(self.request, queryset, self)
            return queryset

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'user__username')

    def get_queryset(self):
        return Task.objects.all()

    def get(self, request):
        filtered_qs = self.filter_queryset(self.get_queryset())
        tasks = filtered_qs
        for i in tasks:
            if i.date <= date.today() and i.status == 'NEW':
                i.delayed = 'This task is delayed'
                i.save()
            else:
                i.delayed = ''
                i.save()

        serializer = IndexSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        tasks = self.get_object(pk)
        if tasks.date <= date.today() and tasks.status == 'NEW':
            tasks.delayed = 'This task is delayed'
            tasks.save()
        else:
            tasks.delayed = ''
            tasks.save()

        serializer = TaskSerializer(tasks)
        return Response(serializer.data)


class TaskUpdateStatusAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get(self, request):
        tasks = self.get_queryset()
        for i in tasks:
            if i.date <= date.today() and i.status == 'NEW':
                i.delayed = 'This task is delayed'
                i.save()
            else:
                i.delayed = ''
                i.save()
        serializer = MyTasksSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
