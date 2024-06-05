from django.urls import path
from . import views

urlpatterns = [
    path("", views.todos, name="Fetching todos"),
    path("<uuid:id>", views.todo, name="Todo Created"),
]
