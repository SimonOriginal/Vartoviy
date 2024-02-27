from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from dashboard.models import DeviceInfo
from .models import Notification

@receiver(post_save, sender=DeviceInfo)
def battery_charge_notification(sender, instance, **kwargs):
    if instance.battery_charge < 20:
        message = _('Низкий заряд батареи! Текущий заряд устройства {device}: {charge}%').format(
            device=instance.device, charge=instance.battery_charge
        )
        create_notification(instance.device, message)

@receiver(post_save, sender=DeviceInfo)
def satellite_count_notification(sender, instance, **kwargs):
    if instance.satellite_count == 0:
        message = _('Нет спутниковой связи у устройства {device}!').format(device=instance.device)
        create_notification(instance.device, message)

@receiver(post_save, sender=DeviceInfo)
def location_notification(sender, instance, **kwargs):
    # Предполагается, что если значение 'inside_or_not' равно False, то устройство находится за пределами барьера
    if not instance.inside_or_not:
        message = _('Устройство {device} покинуло барьер!').format(device=instance.device)
        create_notification(instance.device, message)

# Вспомогательная функция для создания уведомлений
def create_notification(device, message):
    Notification.objects.create(device=device, message=message)
