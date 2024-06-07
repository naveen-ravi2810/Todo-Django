from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from .models import Users
from datetime import datetime, timedelta
from django.utils import timezone
from project_struct.utils import (
    hashed_password,
    check_password,
    create_access_token,
    auth_required,
    decode_access_token,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = Users(**serializer.validated_data)
            user.password = hashed_password(serializer.validated_data["password"])
            user.save()
            return Response(
                {"message": "User Created Successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = Users.objects.filter(
                email=serializer.validated_data["email"]
            ).first()
            # If the userr email is not exist
            if not user:
                return Response(
                    {"message": "Invalid Password/Username"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # If the user is not active
            if not user.is_active:
                return Response(
                    {"message": "User is not in active"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # If the user not logged in for 10 days
            if (timezone.now() - user.last_logged_in) >= timedelta(days=10):
                user.is_active = False
                user.save()
                return Response(
                    {"message": "The user is inactive"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # Check the user password
            if check_password(serializer.validated_data["password"], user.password):
                token = create_access_token(user)
                user.last_logged_in = datetime.now()
                user.save()
                return Response({"access_token": token}, status=status.HTTP_200_OK)
            return Response(
                {"message": "Invalid Password/Username"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class TokenView(APIView):
    @auth_required
    def get(self, request: HttpRequest):
        token_details = decode_access_token(
            request.headers.get("Authorization").split(" ")[1]
        )
        return Response({"user": token_details}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    @auth_required
    def get(self, request):
        user = Users.objects.filter(id=request.user_id).first()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)