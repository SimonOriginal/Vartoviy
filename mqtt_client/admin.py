# admin.py
from django.contrib import admin
from .models import MQTTConnection

class MQTTConnectionAdmin(admin.ModelAdmin):
    list_display = ('mqtt_broker', 'mqtt_port', 'mqtt_username', 'mqtt_password')
    search_fields = ('mqtt_broker',)
    list_filter = ('mqtt_port',)
    ordering = ('mqtt_broker',)

admin.site.register(MQTTConnection, MQTTConnectionAdmin)
