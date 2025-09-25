import uuid

from django.contrib.auth.models import User
from django.db import models

from src.domain.core.category import CategoryEntity

class ExpenseEntity(models.Model):
    id : models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value : models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    spent_at : models.DateTimeField = models.DateTimeField(auto_now_add=True)
    description : models.TextField = models.TextField(null=True, blank=True)
    creator : models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    categories : models.ManyToManyField = models.ManyToManyField(CategoryEntity)
    created_at : models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at : models.DateTimeField = models.DateTimeField(auto_now=True)
