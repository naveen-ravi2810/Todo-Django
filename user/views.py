from django.http import JsonResponse
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Users
from project_struct.utils import hashed_password, check_password

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = Users(**serializer.validated_data)
        user.password = hashed_password(serializer.validated_data['password'])
        user.save()
        return JsonResponse({'message':'User Created Successfully'}, status=status.HTTP_201_CREATED)
    return JsonResponse({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = Users.objects.filter(email=serializer.validated_data['email']).first()
        if not user:
            return JsonResponse({'message':'Invalid Password/Username'}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(serializer.validated_data['password'], user.password):
            return JsonResponse({'message':'Logged In'}, status=status.HTTP_200_OK)
        return JsonResponse({'message':'Invalid Password/Username'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)