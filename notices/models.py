# models.py
from django.db import models
from django.utils import timezone
from dashboard.models import Device

class Notification(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    message = models.CharField(max_length=255, verbose_name='Сообщение')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Дата и время')
    viewed = models.BooleanField(default=False, verbose_name='Просмотрено')

    def __str__(self):
        return f"{self.timestamp} - {self.message}"
    
    class Meta:
        verbose_name = 'Уведомление'  # Название модели в единственном числе
        verbose_name_plural = 'Уведомления'  # Название модели во множественном числе
