from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Task
from .serializer import TaskSerializer, TaskIndexSerializer, MyTasksSerializer


class TaskViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskIndexAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskIndexSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'user__username')


class TaskDetailAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get(self, request):
        tasks = self.get_queryset()
        serializer = MyTasksSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MyTasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
