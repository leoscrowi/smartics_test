from rest_framework import serializers

from src.domain.core.category.models import CategoryEntity
from src.domain.core.expense.models import ExpenseEntity

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryEntity
        fields = ('id', 'name',)

class ExpenseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = ExpenseEntity
        fields = ('id', 'value', 'spent_at', 'description', 'categories', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
