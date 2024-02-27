from django.db import models
from users.models import User

# Модель для хранения геозон
class GeoZone(models.Model):
    # Поле для хранения геоданных в формате GeoJSON
    geojson = models.TextField(verbose_name='Геоданные')
    # Поле для хранения названия геозоны
    name = models.CharField(max_length=100, verbose_name='Название геозоны')
    # Поле для хранения даты и времени создания геозоны
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    # Внешний ключ для связи с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='Пользователь')
    device = models.ForeignKey('dashboard.Device', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Устройство', related_name='geo_zones')

    # Метод для возвращения строкового представления объекта
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Геозону'  # Название модели в единственном числе
        verbose_name_plural = 'Геозоны пользователей'  # Название модели во множественном числе
