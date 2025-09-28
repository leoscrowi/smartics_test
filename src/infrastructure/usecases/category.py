import uuid
from typing import List

from src.domain.core.category.models import CategoryEntity

class CategoryUsecase:

    def __init__(self, category_repo: object):
        self.category_repo = category_repo

    def get(self, category_id: uuid.UUID) -> CategoryEntity:
        return self.category_repo.get(category_id)

    def get_user_categories(self, user_id: uuid.UUID) -> List[CategoryEntity]:
        return self.category_repo.get_user_categories(user_id)

    def save(self, category: CategoryEntity) -> CategoryEntity:
        return self.category_repo.save(category)

    def delete(self, category_id: uuid.UUID):
        self.category_repo.delete(category_id)

    def update(self, category: CategoryEntity) -> CategoryEntity:
        return self.category_repo.update(category)
