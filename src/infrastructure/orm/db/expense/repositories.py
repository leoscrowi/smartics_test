import uuid
from typing import List

from src.domain.core.expense.models import ExpenseEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class ExpenseDatabaseRepository:

    def get(self, expense_id: uuid.UUID) -> ExpenseEntity:
        expense = ExpenseEntity.objects.get(id=expense_id)
        if not expense:
            raise EntityDoesNotExist(f'expense with id {expense_id} does not exist')
        return ExpenseEntity(**expense)

    def get_user_expenses(self, user_id: uuid.UUID) -> List[ExpenseEntity]:
        return list(ExpenseEntity.objects.filter(creator_id=user_id))

    def save(self, expense: ExpenseEntity) -> ExpenseEntity:
        try:
            if not expense.id:
                expense.id = uuid.uuid4()
                expense.save()
                return expense
            raise EntityExists(f'category with id: {expense.id} already exists')
        except Exception:
            raise EntityDatabaseError(f"Error saving category")

    def delete(self, expense_id: uuid.UUID):
        try:
            category = ExpenseEntity.objects.get(id=expense_id)
            category.delete()
        except ExpenseEntity.DoesNotExist:
            raise EntityDoesNotExist(f'category with id: {expense_id} does not exist')
        except Exception:
            raise EntityDatabaseError(f'Error deleting category')

    def update(self, expense: ExpenseEntity) -> ExpenseEntity:
        try:
            if expense.id:
                expense = ExpenseEntity.objects.get(id=expense.id)
                if expense:
                    for field, value in expense.__dict__.items():
                        if not field.startswith('_'):
                            setattr(expense, field, value)
                expense.save()
            else:
                expense.id = uuid.uuid4()
                expense.save()
            return expense
        except Exception:
            raise EntityDatabaseError(f"Error updating category")
