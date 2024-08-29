from django.urls import path

from .api import (
    liquidaciones
)

urlpatterns = [
    path('', liquidaciones)
]