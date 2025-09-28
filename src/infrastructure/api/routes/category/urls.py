from django.urls import path, include
from rest_framework import routers

from src.infrastructure.api.views.category import CategoryViewSet
from src.infrastructure.factories.category import CategoryControllerFactory

CategoryViewSet.viewset_factory = CategoryControllerFactory()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]