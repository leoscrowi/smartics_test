import uuid

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    id : models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name : models.TextField = models.TextField()
    creator : models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at : models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at : models.DateTimeField = models.DateTimeField(auto_now=True)
