from django.apps import AppConfig

class MqttClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_client'
    verbose_name = 'Параметры MQTT'

    def ready(self):
        import mqtt_client.signals

