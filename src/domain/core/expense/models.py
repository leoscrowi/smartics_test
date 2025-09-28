import uuid

from django.contrib.auth.models import User
from django.db import models

from src.domain.core.category.models import CategoryEntity

class ExpenseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    spent_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(CategoryEntity, through='ExpenseCategory', related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'expense'


class ExpenseCategory(models.Model):
    expense = models.ForeignKey(ExpenseEntity, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryEntity, on_delete=models.CASCADE)

    class Meta:
        app_label = 'expense'