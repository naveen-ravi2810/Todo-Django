from django.db import models
from uuid import uuid4


# Create your models here.
class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=20)
    email = models.EmailField(max_length=60, unique=True)
    password = models.TextField(max_length=300)
