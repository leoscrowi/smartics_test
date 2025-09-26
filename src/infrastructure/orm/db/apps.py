from django.apps import AppConfig

class CategoryConfig(AppConfig):
    label = 'categories'
    name = 'src.infrastructure.orm.db.category'
    verbose_name = 'Categories'

class ExpenseConfig(AppConfig):
    label = 'expenses'
    name = 'src.infrastructure.orm.db.expense'
    verbose_name = 'Expense'