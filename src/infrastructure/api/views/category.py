import logging
import uuid

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.utils import timezone

from src.domain.core.category.models import CategoryEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError
from src.infrastructure.contracts.serializers.category import CategorySerializer
from src.infrastructure.controllers.category import CategoryController

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    @property
    def controller(self) -> CategoryController:
        return self.viewset_factory.get()

    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(pk)
            category = self.controller.get(category_id)

            if category.creator_id != request.user.id:
                return Response({"error": "not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(category)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category_data = serializer.validated_data
            category_entity = CategoryEntity(
                name=category_data['name'],
                creator=request.user,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            self.controller.save(category=category_entity)
            response_serializer = self.get_serializer(category_entity)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except EntityExists as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except EntityDatabaseError as e:
            return Response({"error": str(e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_INTERNAL_SERVER_ERROR)


    def destroy(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(pk)
            category = self.controller.get(category_id)

            if category.creator_id != request.user.id:
                return Response({"error": "not allowed"}, status=status.HTTP_403_FORBIDDEN)

            self.controller.delete(category_id)
            return Response(status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(pk)
            ex_category = self.controller.get(category_id)
            if ex_category.creator_id != request.user.id:
                return Response({"error": "not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category_data = serializer.validated_data

            self.controller.update(CategoryEntity(
                id=category_id,
                name=category_data['name'],
                updated_at=timezone.now(),
                created_at=timezone.now(),
            ))
            return Response(status=status.HTTP_200_OK)
        except EntityDatabaseError as e:
            return Response({"error": "entity database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request: Request, *args, **kwargs) -> Response:
        try:
            categories = self.controller.get_user_categories(request.user.id)
            serializer = self.get_serializer(categories, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)