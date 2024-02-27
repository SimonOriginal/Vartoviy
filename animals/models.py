from django.db import models
from users.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class Animal(models.Model):

    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]

    name = models.CharField(max_length=255, verbose_name='Имя животного')
    species = models.CharField(max_length=50, verbose_name='Вид')
    breed = models.CharField(max_length=50, verbose_name='Порода')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_('Пол'))
    age = models.IntegerField(verbose_name='Возраст')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='animals')
    device = models.OneToOneField('dashboard.Device', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Устройство')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные' 
    
class Photo(models.Model):
    animal = models.ForeignKey(Animal, related_name='animal_photos', on_delete=models.CASCADE, verbose_name='Животное')
    image = models.ImageField(upload_to='animal_photos/', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фото' 
        verbose_name_plural = 'Фотографии'  

@receiver(pre_delete, sender=Animal)
def delete_animal_photos(sender, instance, **kwargs):
    # Удаляем все фотографии, связанные с животным
    for photo in instance.animal_photos.all():
        photo.image.delete(save=False)

