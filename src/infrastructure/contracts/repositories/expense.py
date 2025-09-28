import uuid
from typing import List, Optional

from src.domain.core.expense.models import ExpenseEntity

class ExpenseRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get(self, expense_id: uuid.UUID) -> Optional[ExpenseEntity]:
        return self.db_repo.get(expense_id)

    def get_user_expenses(self, user_id) -> List[ExpenseEntity]:
        return self.db_repo.get_user_expenses(user_id)

    def save(self, expense: ExpenseEntity) -> Optional[ExpenseEntity]:
        self.db_repo.save(expense)

    def delete(self, expense_id: uuid.UUID):
        self.db_repo.delete(expense_id)

    def update(self, expense: ExpenseEntity):
        self.db_repo.update(expense)
