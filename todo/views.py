from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from .models import Todos
from user.models import Users
from .serializers import ReadTodosSerializer, CreateTodoSerializer
from uuid import UUID


# To fetch every Todos or create a todo
@api_view(['GET', 'POST'])
def todos(request):
    if request.method=='GET':
        todos = Todos.objects.all()
        serializer = ReadTodosSerializer(todos, many=True)
        return JsonResponse({'todos':serializer.data}, status=status.HTTP_200_OK)
    if request.method=='POST':
        serializer = CreateTodoSerializer(data=request.data)
        if serializer.is_valid():
            new_todo = Todos(**serializer.validated_data)
            new_todo.user_id=Users.objects.first()
            new_todo.save()
            return JsonResponse({'message':"Todo added successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# To make an operation on a single todo
@api_view(['GET', 'PUT', 'DELETE'])
def todo(request, id:UUID):
    todo = Todos.objects.filter(id=id).first()
    if not todo:
        return JsonResponse({'message':'Todo Not Found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = ReadTodosSerializer(todo)
        return JsonResponse({'todo':serializer.data}, status=status.HTTP_200_OK)
    if request.method=='PUT':
        todo.status = not todo.status
        todo.save()
        return JsonResponse({'message':'Todo updated successfully'}, status=status.HTTP_202_ACCEPTED)
    if request.method=='DELETE':
        todo.delete()
        return JsonResponse({'message':'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
