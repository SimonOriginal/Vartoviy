# Generated by Django 4.2.6 on 2023-11-09 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about_us_app', '0002_alter_developer_options_alter_faq_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='developer',
            options={'verbose_name': 'Разработчика', 'verbose_name_plural': 'Разработчики'},
        ),
    ]
