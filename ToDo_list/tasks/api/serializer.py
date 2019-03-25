from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'name', 'user', 'status', 'date', 'description', 'delayed')


class IndexSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'date', 'status', 'user', 'delayed')


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('status',)


class MyTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'status', 'date', 'description', 'delayed')


class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'date', 'description',)

