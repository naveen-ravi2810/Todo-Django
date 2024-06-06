from django.urls import path
from . import views

urlpatterns = [
    path("", views.ManyTodoView.as_view(), name="todos view"),
    path("<uuid:id>", views.SingleTodoView.as_view(), name="todo view"),
]
