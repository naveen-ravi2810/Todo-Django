from django.db import models
from uuid import uuid4
from datetime import datetime
from user.models import Users


# Create your models here.
class Todos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    task = models.TextField(max_length=100)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
