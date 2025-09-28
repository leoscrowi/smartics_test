import uuid
from typing import List

from src.domain.core.category.models import CategoryEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class CategoryDatabaseRepository:

    def get(self, category_id: uuid.UUID) -> CategoryEntity:
        category = CategoryEntity.objects.get(id=category_id)
        if not category:
            raise EntityDoesNotExist(f'category with id: {category_id} does not exist')
        return category

    def get_user_categories(self, user_id: uuid.UUID) -> List[CategoryEntity]:
        return list(CategoryEntity.objects.filter(creator_id=user_id))

    def save(self, category: CategoryEntity) -> CategoryEntity:
        category.id = uuid.uuid4()
        category.save()
        return category

    def delete(self, category_id: uuid.UUID):
        try:
            category = CategoryEntity.objects.get(id=category_id)
            category.delete()
        except CategoryEntity.DoesNotExist:
            raise EntityDoesNotExist(f'category with id: {category_id} does not exist')
        except Exception:
            raise EntityDatabaseError(f'Error deleting category')

    def update(self, category: CategoryEntity) -> CategoryEntity:
        try:
            if category.id:
                category = CategoryEntity.objects.get(id=category.id)
                if category:
                    for field, value in category.__dict__.items():
                        if not field.startswith('_'):
                            setattr(category, field, value)
                category.save()
                return category
            else:
                category.id = uuid.uuid4()
                category.save()
                return category
        except Exception:
            raise EntityDatabaseError(f'Error updating category')
