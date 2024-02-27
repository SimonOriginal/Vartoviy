import json
import time
import paho.mqtt.client as mqtt
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from geoapp.models import GeoZone
from mqtt_client.models import MQTTConnection

User = get_user_model()
keep_alive = 10
MQTT_QOS = 0

@receiver(post_save, sender=GeoZone)
def geozone_change_handler(sender, instance, created, **kwargs):
    action = "создана" if created else "обновлена"
    device = instance.device

    if device:
        device.last_updated = timezone.now()
        device.save()

    topic = f"device_esp/{device.unit_number}/geozone"
    payload = {"geojson": instance.geojson}

    try:
        publish_to_mqtt(topic, payload)
        print(f"Данные, отправленные MQTT-брокеру: Тема - {topic}, Данные - {payload}")
    except Exception as e:
        print(f"Ошибка при отправке данных брокеру MQTT: {e}")

def publish_to_mqtt(topic, payload):
    try:
        mqtt_connection_settings = MQTTConnection.objects.first()

        # Инициализация MQTT-клиента
        client = mqtt.Client("mqtt_publish")
        client.username_pw_set(username=mqtt_connection_settings.mqtt_username, password=mqtt_connection_settings.mqtt_password)
        client.connect(mqtt_connection_settings.mqtt_broker, mqtt_connection_settings.mqtt_port, keep_alive)

        # Опубликовать сообщение
        client.publish(topic, json.dumps(payload), qos=MQTT_QOS)

        # Дайте некоторое время, чтобы сообщение было отправлено
        time.sleep(0.5)  # Вы можете регулировать продолжительность сна в зависимости от ваших потребностей

        # Отключитесь от брокера
        client.disconnect()
    except (mqtt.MQTTException, json.JSONDecodeError) as e:
        raise Exception(f"Ошибка при отправке данных брокеру MQTT: {e}")
