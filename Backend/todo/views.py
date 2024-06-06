from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todos
from user.models import Users
from .serializers import ReadTodosSerializer, CreateTodoSerializer
from uuid import UUID
from project_struct.utils import auth_required

# To fetch every Todos or create a todo
class ManyTodoView(APIView):
    @auth_required
    def get(self, request):
        todos = Todos.objects.filter(user_id=request.user_id).order_by('created_on').all()
        serializer = ReadTodosSerializer(todos, many=True)
        return Response({"todos": serializer.data}, status=status.HTTP_200_OK)

    @auth_required
    def post(self, request):
        serializer = CreateTodoSerializer(data=request.data)
        if serializer.is_valid():
            new_todo = Todos(**serializer.validated_data)
            new_todo.user_id = Users.objects.filter(id=request.user_id).first()
            new_todo.save()
            serializer = ReadTodosSerializer(new_todo)
            return Response(
                {"todo": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


# To make an operation on a single todo
class SingleTodoView(APIView):
    @auth_required
    def get(self, request, id:UUID):
        todo = Todos.objects.filter(id=id).filter(user_id=request.user_id).first()
        if not todo:
            return Response(
                {"message": "Todo Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReadTodosSerializer(todo)
        return Response({"todo": serializer.data}, status=status.HTTP_200_OK)
    @auth_required
    def put(self, request, id:UUID):
        todo = Todos.objects.filter(id=id).filter(user_id=request.user_id).first()
        if not todo:
            return Response(
                {"message": "Todo Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        todo.status = not todo.status
        todo.save()
        return Response(
            {"message": "Todo updated successfully"}, status=status.HTTP_202_ACCEPTED
        )
    @auth_required    
    def delete(self, request, id:UUID):
        todo = Todos.objects.filter(id=id).filter(user_id=request.user_id).first()
        if not todo:
            return Response(
                {"message": "Todo Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        todo.delete()
        return Response(
            {"message": "Todo deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )