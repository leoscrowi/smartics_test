import uuid
from typing import List

from src.domain.core.expense.models import ExpenseEntity


class ExpenseController:

    def __init__(self, expense_usecase: object):
        self.expense_usecase = expense_usecase

    def get(self, expense_id: uuid.UUID):
        return self.expense_usecase.get(expense_id)

    def save(self, expense: ExpenseEntity) -> ExpenseEntity:
        return self.expense_usecase.save(expense)

    def delete(self, expense_id: uuid.UUID):
        self.expense_usecase.delete(expense_id)

    def update(self, expense: ExpenseEntity) -> ExpenseEntity:
        return self.expense_usecase.update(expense)