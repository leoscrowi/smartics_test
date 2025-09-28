from django.contrib import admin

from src.domain.core.category.models import CategoryEntity
from src.infrastructure.admin.category.admin import CategoryEntityAdmin

admin.site.register(CategoryEntity, CategoryEntityAdmin)