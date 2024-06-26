from typing import Any
import bcrypt
import jwt
from pytz import timezone
from datetime import datetime, timedelta
from functools import wraps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import HttpRequest
from user.models import Users
from project_struct import settings


def hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user: Users) -> str:
    ist = timezone("Asia/Kolkata")
    iat = datetime.now(ist)
    exp = iat + timedelta(days=1)
    return jwt.encode(
        payload={
            "email": user.email,
            "sub": str(user.id),
            "iat": iat,
            "exp": exp,
            "name": user.first_name + " " + user.last_name,
        },
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str):
    return jwt.decode(
        jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
    )


def auth_required(fn):
    @wraps(fn)
    def decorator(self, request: HttpRequest, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if auth_header is None:
            return JsonResponse(
                {"error": "Authorization header missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            schema, token = auth_header.split()[0], auth_header.split()[1]
            if schema.lower() != "bearer":
                return JsonResponse(
                    {"error": "Invalid schema"}, status=status.HTTP_401_UNAUTHORIZED
                )
            if token == None:
                return JsonResponse(
                    {"message": "Token Missing"}, status=status.HTTP_401_UNAUTHORIZED
                )
            jwt_claims = decode_access_token(token)
            request.user_id = jwt_claims["sub"]
            return fn(self, request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )

    return decorator


class Pagination:
    def __init__(self, serializer, request: HttpRequest | None = None) -> None:
        self.content = serializer
        self.request = request
        self.page_no = int(request.GET.get("page_no", 1))
        self.page_count = int(request.GET.get("page_count", 10))

    def previous_page(self):
        if self.page_no <= 1:
            return None
        # return self.request.path +"?page_no="+ str(self.page_no-1)
        return self.page_no - 1

    def next_page(self):
        if self.page_no >= len(self.content) / self.page_count:
            return None
        # return self.request.path +"?page_no="+ str(self.page_no+1)
        return self.page_no + 1

    def data(self):
        return self.content[
            (self.page_no - 1) * self.page_count : self.page_no * self.page_count
        ]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return {
            "previous_page": self.previous_page(),
            "next_page": self.next_page(),
            "total": len(self.content),
            "data": self.data(),
        }
