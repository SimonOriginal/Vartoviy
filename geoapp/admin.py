from django.contrib import admin
from .models import GeoZone

# Класс для настройки отображения модели GeoZone в административной панели
class GeoZoneAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке объектов
    list_display = ('name', 'created_at', 'user', 'device')
    # Поля, по которым можно осуществлять поиск
    search_fields = ('name', 'user', 'device')
    # Поля, которые будут доступны для редактирования
    fields = ('name', 'geojson', 'device')

# Регистрируем модель GeoZone и ее настройки в административной панели
admin.site.register(GeoZone, GeoZoneAdmin)
