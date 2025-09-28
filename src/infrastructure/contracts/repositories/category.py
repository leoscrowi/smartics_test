import uuid
from typing import List, Optional

from src.domain.core.category.models import CategoryEntity

class CategoryRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get(self, category_id: uuid.UUID) -> Optional[CategoryEntity]:
        return self.db_repo.get(category_id)

    def get_user_categories(self, user_id: uuid.UUID) -> List[CategoryEntity]:
        return self.db_repo.get_user_categories(user_id)

    def save(self, category: CategoryEntity) -> Optional[CategoryEntity]:
        self.db_repo.save(category)

    def delete(self, category_id: uuid.UUID):
        self.db_repo.delete(category_id)

    def update(self, category: CategoryEntity):
        self.db_repo.update(category)
