# Generated by Django 4.2.6 on 2023-12-23 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about_us_app', '0004_alter_developer_options_alter_project_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='developer',
            options={'verbose_name': 'Разработчика', 'verbose_name_plural': 'Разработчики'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Описание', 'verbose_name_plural': 'Описание'},
        ),
    ]
