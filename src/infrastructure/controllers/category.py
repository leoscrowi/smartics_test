import uuid
from typing import List

from src.domain.core.category.models import CategoryEntity


class CategoryController:

    def __init__(self, category_usecase: object):
        self.category_usecase = category_usecase

    def get(self, category_id: uuid.UUID) -> CategoryEntity:
        return self.category_usecase.get(category_id)

    def get_user_categories(self, user_id: uuid.UUID) -> List[CategoryEntity]:
        return self.category_usecase.get_user_categories(user_id)

    def save(self, category: CategoryEntity) -> CategoryEntity:
        return self.category_usecase.save(category)

    def delete(self, category_id: uuid.UUID):
        self.category_usecase.delete(category_id)

    def update(self, category: CategoryEntity) -> CategoryEntity:
        return self.category_usecase.update(category)