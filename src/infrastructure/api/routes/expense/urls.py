from rest_framework import routers

from src.infrastructure.api.views.expense import ExpenseViewSet

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expenses')

