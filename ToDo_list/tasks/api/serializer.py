from rest_framework import serializers

from ..models import Task


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'name', 'creator', 'status', 'completion_date', 'description', 'warning_of_delaying')


class TasksIndexSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'completion_date', 'status', 'creator', 'warning_of_delaying')


class UpdateTaskStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('status',)


class UserTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'status', 'completion_date', 'description', 'warning_of_delaying')


class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'completion_date', 'description',)

