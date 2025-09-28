from django.conf import settings
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from src.infrastructure.api.views.register import RegisterViewSet

urlpatterns = [
    # for my own entities
    path('', include(f'{settings.API_ROUTES}.category.urls')),
    path('', include(f'{settings.API_ROUTES}.expense.urls')),

    # for register
    path('register', RegisterViewSet.as_view(), name='register'),

    # for jwt auth
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]