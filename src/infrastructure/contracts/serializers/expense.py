from rest_framework import serializers

from src.domain.core.category.models import CategoryEntity
from src.domain.core.expense.models import ExpenseEntity

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryEntity
        fields = ('id', 'name',)

class ExpenseSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseEntity
        fields = ('id', 'value', 'spent_at', 'description', 'categories', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data

class ExpenseCreateSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = ExpenseEntity
        fields = ('value', 'spent_at', 'description', 'categories')

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        expense = ExpenseEntity.objects.create(**validated_data)

        for category_id in categories_data:
            try:
                category = CategoryEntity.objects.get(id=category_id)
                expense.categories.add(category)
            except CategoryEntity.DoesNotExist:
                raise serializers.ValidationError(f"Category with id {category_id} does not exist")

        return expense