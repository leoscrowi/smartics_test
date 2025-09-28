from django.urls import path, include
from rest_framework import routers

from src.infrastructure.api.views.expense import ExpenseViewSet
from src.infrastructure.factories.expense import ExpenseControllerFactory

ExpenseViewSet.viewset_factory = ExpenseControllerFactory()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls))
]