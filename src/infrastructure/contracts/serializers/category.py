from rest_framework import serializers

from src.domain.core.category.models import CategoryEntity


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryEntity
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')