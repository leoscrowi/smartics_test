import uuid
from typing import List

from src.domain.core.category.models import CategoryEntity
from src.infrastructure.contracts.repositories.exceptions import EntityDoesNotExist, EntityExists, EntityDatabaseError


class CategoryDatabaseRepository:

    def get(self, category_id: uuid.UUID) -> CategoryEntity:
        try:
            category = CategoryEntity.objects.get(id=category_id)
            return category
        except CategoryEntity.DoesNotExist:
            raise EntityDoesNotExist(f'category with id: {category_id} does not exist')

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
            raise EntityDatabaseError(f'error deleting category')

    def update(self, category: CategoryEntity) -> CategoryEntity:
        try:
            if category.id:
                existing_category = CategoryEntity.objects.get(id=category.id)
                if existing_category:
                    updatable_fields = ['name', 'updated_at']
                    for field in updatable_fields:
                        if hasattr(category, field):
                            setattr(existing_category, field, getattr(category, field))
                existing_category.save()
                return category
            else:
                category.id = uuid.uuid4()
                category.save()
                return category
        except Exception as e:
            raise EntityDatabaseError(f'error updating category: {str(e)}')
