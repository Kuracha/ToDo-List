from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'name', 'user', 'status', 'date', 'description')


class TaskIndexSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ('name', 'date', 'status', 'user')


class MyTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'status', 'date', 'description')
