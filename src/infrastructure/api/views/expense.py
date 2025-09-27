from src.infrastructure.controllers.expense import ExpenseController
import uuid

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.utils import timezone

from src.domain.core.expense.models import ExpenseEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class ExpenseViewSet(viewsets.ModelViewSet):

    @property
    def controller(self) -> ExpenseController:
        return self.viewset_factory.create()

    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            expense_id = uuid.UUID(str(pk))
            expense = self.controller.get(expense_id)

            if expense.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(expense)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            expense_data = serializer.validated_data
            expense_entity = ExpenseEntity(
                value=expense_data['value'],
                description=expense_data['description'],
                creator=request.user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            if 'categories' in expense_data:
                expense_entity.categories.set(expense_data['categories'])
            self.controller.create(expense_entity)
            response_serializer = self.get_serializer(expense_entity)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except EntityExists:
            return Response(status=status.HTTP_409_CONFLICT)
        except EntityDatabaseError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            expense_id = uuid.UUID(str(pk))
            expense = self.controller.get(expense_id)

            if expense.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            self.controller.delete(expense_id)
            return Response(status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            expense_id = uuid.UUID(str(pk))
            ex_expense_id = self.controller.get(expense_id)
            if ex_expense_id.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            expense_data = serializer.validated_data

            updated_expense = self.controller.update(ExpenseEntity(
                id=expense_id,
                value=expense_data['value'],
                spent_at=expense_data['spent_at'],
                description=expense_data['description'],
                categories=expense_data['categories'],
                updated_at = timezone.now(),
            ))
            response_serializer = self.get_serializer(updated_expense)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except EntityDatabaseError:
            return Response({"error": "Entity database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
