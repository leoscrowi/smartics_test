from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', include(f'{settings.API_ROUTES}.category.urls')),
    path('', include(f'{settings.API_ROUTES}.expenses.urls'))
]