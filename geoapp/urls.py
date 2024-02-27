from django.urls import path
from . import views

urlpatterns = [
    # Путь для главной страницы
    path('', views.ConfigurationView.as_view(), name='configuration'),
    # Путь для сохранения геозоны в базу данных
    path('save_geozone/', views.save_geozone, name='save_geozone'),
    # Путь для получения geojson данных
    path('get_geojson/', views.get_geojson, name='get_geojson'),
]
