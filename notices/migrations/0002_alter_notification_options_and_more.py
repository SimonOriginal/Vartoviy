# Generated by Django 4.2.6 on 2023-11-21 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_devices_device'),
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AddField(
            model_name='notification',
            name='battery_charge',
            field=models.FloatField(blank=True, null=True, verbose_name='Уровень заряда батареи'),
        ),
        migrations.AddField(
            model_name='notification',
            name='location_status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Статус местоположения'),
        ),
        migrations.AddField(
            model_name='notification',
            name='satellite_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество спутников'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='dashboard.device', verbose_name='Устройство'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время уведомления'),
        ),
    ]
