import uuid

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.utils import timezone

from src.domain.core.expense import ExpenseEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class CategoryViewSet(viewsets.ModelViewSet):

    @property
    def controller(self) -> CategoryController:
        return self.viewset_factory.create()

    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(str(pk))
            category = self.controller.get(category_id)

            if category.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(category)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category_data = serializer.validated_data
            category_entity = ExpenseEntity(
                value=category_data['name'],
                description=category_data['description'],
                creator=request.user,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            self.controller.create(expense=category_entity)
            response_serializer = self.get_serializer(category_entity)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except EntityExists:
            return Response(status=status.HTTP_409_CONFLICT)
        except EntityDatabaseError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(str(pk))
            category = self.controller.get(category_id)

            if category.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            self.controller.delete(category_id)
            return Response(status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            category_id = uuid.UUID(str(pk))
            ex_category = self.controller.get(category_id)
            if ex_category.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category_data = serializer.validated_data

            updated_category = self.controller.update(ExpenseEntity(
                id=category_id,
                name=category_data['name'],
                description=category_data['description'],
                updated_at=timezone.now(),
            ))
            response_serializer = self.get_serializer(updated_category)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except EntityDatabaseError:
            return Response({"error": "Entity database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
