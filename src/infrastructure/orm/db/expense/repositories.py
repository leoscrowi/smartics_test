import uuid
from typing import List

from src.domain.core.expense.models import ExpenseEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class ExpenseDatabaseRepository:

    def get(self, expense_id: uuid.UUID) -> ExpenseEntity:
        try:
            expense = ExpenseEntity.objects.get(id=expense_id)
            return expense
        except ExpenseEntity.DoesNotExist:
            raise EntityDoesNotExist(f'expense with id: {expense_id} does not exist')

    def get_user_expenses(self, user_id: uuid.UUID) -> List[ExpenseEntity]:
        return list(ExpenseEntity.objects.filter(creator_id=user_id))

    def save(self, expense: ExpenseEntity) -> ExpenseEntity:
        expense.id = uuid.uuid4()
        expense.save()
        return expense

    def delete(self, expense_id: uuid.UUID):
        try:
            category = ExpenseEntity.objects.get(id=expense_id)
            category.delete()
        except ExpenseEntity.DoesNotExist:
            raise EntityDoesNotExist(f'category with id: {expense_id} does not exist')
        except Exception:
            raise EntityDatabaseError(f'error deleting category')

    def update(self, expense: ExpenseEntity) -> ExpenseEntity:
        try:
            if expense.id:
                existing_expense = ExpenseEntity.objects.get(id=expense.id)
                if existing_expense:
                    updatable_fields = ['value', 'description', 'categories']
                    for field in updatable_fields:
                        if hasattr(expense, field):
                            setattr(existing_expense, field, getattr(expense, field))
                existing_expense.save()
                return expense
            else:
                expense.id = uuid.uuid4()
                expense.save()
            return expense
        except Exception:
            raise EntityDatabaseError(f"Error updating category")
