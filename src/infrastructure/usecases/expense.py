import uuid
from typing import List

from src.domain.core.expense.models import ExpenseEntity


class ExpenseUsecase:

    def __init__(self, expense_repo: object):
        self.expense_repo = expense_repo

    def get(self, expense_id: uuid.UUID) -> ExpenseEntity:
        return self.expense_repo.get(expense_id)

    def save(self, expense: ExpenseEntity) -> ExpenseEntity:
        return self.expense_repo.save(expense)

    def delete(self, expense_id: uuid.UUID):
        self.expense_repo.delete(expense_id)

    def update(self, expense: ExpenseEntity) -> ExpenseEntity:
        return self.expense_repo.update(expense)
