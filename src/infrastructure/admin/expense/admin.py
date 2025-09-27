from django.contrib import admin

from src.domain.core.category import CategoryEntity
from src.domain.core.expense import ExpenseCategory


class ExpenseCategoryInline(admin.TabularInline):
    model = ExpenseCategory
    extra = 0

class ExpenseEntityAdmin(admin.ModelAdmin):
    inlines = [ExpenseCategoryInline]
    list_display = ('id', 'value', 'spent_at', 'creator')
    search_fields = ('description',)
    list_filter = ('spent_at', 'creator')
    readonly_fields = ('spent_at', 'created_at', 'updated_at')

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('expense', 'category')