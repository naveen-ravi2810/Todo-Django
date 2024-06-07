from django.urls import path
from . import views

urlpatterns = [
    path(
        "register",
        views.RegisterView.as_view(),
        name="register user",
    ),
    path("login", views.LoginView.as_view(), name="login user"),
    path("token", views.TokenView.as_view(), name="user token"),
    path("profile", views.ProfileView.as_view(), name="profile")
]
