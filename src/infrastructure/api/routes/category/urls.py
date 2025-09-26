from rest_framework import routers

from src.infrastructure.api.views.category import CategoryViewSet
from src.infrastructure.factories.expense import ExpenseControllerFactory

CategoryViewSet.viewset_factory = ExpenseControllerFactory()

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')

