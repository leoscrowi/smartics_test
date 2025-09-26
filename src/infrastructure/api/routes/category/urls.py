from rest_framework import routers

from src.infrastructure.api.views.category import CategoryViewSet
from src.infrastructure.factories.category import CategoryControllerFactory

CategoryViewSet.viewset_factory = CategoryControllerFactory()

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')

