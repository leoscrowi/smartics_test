from src.domain.core.category.models import CategoryEntity
from src.infrastructure.contracts.serializers.expense import ExpenseSerializer, ExpenseCreateSerializer
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
    serializer_class = ExpenseSerializer
    queryset = CategoryEntity.objects.all()

    @property
    def controller(self) -> ExpenseController:
        return self.viewset_factory.get()

    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        try:
            expense_id = uuid.UUID(pk)
            expense = self.controller.get(expense_id)

            if expense.creator_id != request.user.id:
                return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            expense = ExpenseEntity.objects.prefetch_related('categories').get(id=expense.id)

            serializer = self.get_serializer(expense)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except EntityDoesNotExist:
            return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            create_serializer = ExpenseCreateSerializer(data=request.data)
            create_serializer.is_valid(raise_exception=True)
            expense_data = create_serializer.validated_data
            expense_entity = ExpenseEntity(
                value=expense_data['value'],
                spent_at=expense_data.get('spent_at', timezone.now()),
                description=expense_data.get('description'),
                creator=request.user,
            )

            self.controller.save(expense_entity)
            if 'categories' in expense_data:
                categories = CategoryEntity.objects.filter(
                    id__in=expense_data['categories'],
                    creator=request.user
                )

                if len(categories) != len(expense_data['categories']):
                    found_ids = set(str(cat.id) for cat in categories)
                    requested_ids = set(str(cat_id) for cat_id in expense_data['categories'])
                    missing_ids = requested_ids - found_ids
                    return Response(
                        {"error": f"categories not found or not accessible: {list(missing_ids)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                expense_entity.categories.set(categories)

            response_serializer = ExpenseSerializer(expense_entity)
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

            self.controller.update(ExpenseEntity(
                id=expense_id,
                value=expense_data['value'],
                description=expense_data['description'],
                updated_at = timezone.now(),
            ))
            return Response(status=status.HTTP_200_OK)
        except EntityDatabaseError as e:
            return Response({"error": "entity database error " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
