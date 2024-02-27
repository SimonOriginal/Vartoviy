# Generated by Django 4.2.6 on 2023-11-30 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MQTTConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mqtt_broker', models.CharField(max_length=255)),
                ('mqtt_port', models.PositiveIntegerField()),
                ('mqtt_username', models.CharField(blank=True, max_length=255, null=True)),
                ('mqtt_password', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Параметры MQTT',
                'verbose_name_plural': 'Параметры MQTT',
            },
        ),
    ]
