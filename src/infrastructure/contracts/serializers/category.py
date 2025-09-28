from rest_framework import serializers

from src.domain.core.category.models import CategoryEntity


class CategorySerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CategoryEntity
        fields = ('id', 'name', 'creator', 'created_at', 'updated_at')
        read_only_fields = ('id', 'creator', 'created_at', 'updated_at')