from django.db import models
from users.models import User

class Device(models.Model):
    unit_number = models.IntegerField(verbose_name='Идентификатор устройства')
    device_name = models.CharField(max_length=100, blank=True, verbose_name='Имя устройства')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='devices')

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

class DeviceInfo(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройства', related_name='info')
    battery_charge = models.FloatField(verbose_name='Уровень заряда батареи', null=True)
    satellite_count = models.IntegerField(verbose_name='Количество спутников', null=True)
    latitude = models.FloatField(verbose_name='Широта', null=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True)
    inside_or_not = models.BooleanField(verbose_name='Внутри или снаружи', null=True)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    def __str__(self):
        return f"{self.device.device_name} - {self.date_time}"

    class Meta:
        verbose_name = 'Информация об устройстве'
        verbose_name_plural = 'Информация об устройствах'

class DeviceMeasurements(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройства', related_name='measurements')
    measurement_id = models.AutoField(primary_key=True, verbose_name='Идентификатор измерения')
    cumulative_angle = models.FloatField(verbose_name='Температура за °F', null=True)
    pressure = models.FloatField(verbose_name='Атмосферное давление', null=True)
    altitude = models.FloatField(verbose_name='Высота над уровнем моря', null=True)
    temperature = models.FloatField(verbose_name='Температура за °C', null=True)
    humidity = models.FloatField(verbose_name='Влажность воздуха', null=True)
    taser_activations = models.IntegerField(verbose_name='Количество активаций тазера', null=True)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения устройств'
