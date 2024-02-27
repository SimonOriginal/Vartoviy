from django.urls import path
from .views import AnimalDetailView

urlpatterns = [
    path('', AnimalDetailView.as_view(), name='animal_detail'),
    # Добавьте другие URL-пути, если необходимо
]
