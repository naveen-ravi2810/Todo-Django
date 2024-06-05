from rest_framework import serializers
from .models import Todos


class ReadTodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ["id", "task", "status", "created_on"]


class CreateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ["task"]
