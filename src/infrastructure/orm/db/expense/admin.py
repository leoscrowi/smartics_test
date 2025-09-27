from django.contrib import admin

from src.domain.core.expense.models import ExpenseEntity, ExpenseCategory
from src.infrastructure.admin.expense.admin import ExpenseEntityAdmin, ExpenseCategoryAdmin

admin.site.register(ExpenseEntity, ExpenseEntityAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)