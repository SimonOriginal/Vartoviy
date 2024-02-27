# models.py
from django.db import models

class MQTTConnection(models.Model):
    mqtt_broker = models.CharField(max_length=255, verbose_name='Брокер', blank=True, null=True)
    mqtt_port = models.PositiveIntegerField(verbose_name='Порт')
    mqtt_username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя пользователя')
    mqtt_password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Пароль')

    def __str__(self):
        return self.mqtt_broker
    
    class Meta:
        verbose_name = 'Параметры MQTT'  # Название модели в единственном числе
        verbose_name_plural = 'Параметры MQTT'  # Название модели во множественном числе

