import os
import django
import paho.mqtt.client as mqtt

# Установите модуль настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guardian.settings")
django.setup()

# Импорт моделей Django после настройки параметров
from dashboard.models import Device, DeviceInfo, DeviceMeasurements
from mqtt_client.models import MQTTConnection
from django.db import transaction

keep_alive = 60

# Определите словарь для накопления данных для каждого устройства
device_data_accumulator = {}

@transaction.atomic
def save_device_data(device, data):
    try:
        DeviceInfo.objects.create(
            device=device,
            battery_charge=data.get('battery_charge'),
            satellite_count=data.get('satellite_count'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            inside_or_not=data.get('inside_or_not')
        )

        DeviceMeasurements.objects.create(
            device=device,
            cumulative_angle=data.get('cumulative_angle'),
            pressure=data.get('pressure'),
            altitude=data.get('altitude'),
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            taser_activations=data.get('taser_activations')
        )

        # Очистка накопленных данных после успешного сохранения
        device_data_accumulator.pop(device.unit_number, None)

        print("Успешно сохранено в базу данных !")

    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

# Пример использования в функции on_message:
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload

    topic_parts = topic.split('/')

    if len(topic_parts) >= 3:
        _, unit_number, _ = topic_parts
        try:
            unit_number = int(unit_number)
        except ValueError:
            print("Неверный формат номера устройства")
            return

        # Инициализируйте данные устройства в аккумуляторе, если они не существуют
        if unit_number not in device_data_accumulator:
            device_data_accumulator[unit_number] = {}

        try:
            device = Device.objects.get(unit_number=unit_number)
            # print(f"Устройство с номером {unit_number} найдено")

            # Извлечение и сохранение данных в аккумуляторе
            if topic == f"device_esp/{unit_number}/battery_charge":
                device_data_accumulator[unit_number]['battery_charge'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/satellite_count":
                device_data_accumulator[unit_number]['satellite_count'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/gps":
                if payload.startswith(b'[') and payload.endswith(b']'):
                    payload = payload[1:-1]
                latitude, longitude = map(float, payload.decode('utf-8').split(','))
                device_data_accumulator[unit_number]['latitude'] = latitude
                device_data_accumulator[unit_number]['longitude'] = longitude
            elif topic == f"device_esp/{unit_number}/zone_status":
                device_data_accumulator[unit_number]['inside_or_not'] = int(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/shocker":
                device_data_accumulator[unit_number]['taser_activations'] = int(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/temperatureFahrenheit":
                device_data_accumulator[unit_number]['cumulative_angle'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/pressure":
                device_data_accumulator[unit_number]['pressure'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/altitude":
                device_data_accumulator[unit_number]['altitude'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/temperatureCelsius":
                device_data_accumulator[unit_number]['temperature'] = float(payload.decode('utf-8'))
            elif topic == f"device_esp/{unit_number}/humidity":
                device_data_accumulator[unit_number]['humidity'] = float(payload.decode('utf-8'))
            else:
                print("Неизвестная тема:", topic)

            # Проверьте наличие всех необходимых данных
            if all(key in device_data_accumulator[unit_number] for key in [
                    'battery_charge', 'satellite_count', 'latitude', 'longitude', 'inside_or_not',
                    'cumulative_angle', 'pressure', 'altitude', 'temperature', 'humidity', 'taser_activations'
            ]):
                save_device_data(device, device_data_accumulator[unit_number])

        except Device.DoesNotExist:
            print(f"Устройство с номером {unit_number} не найдено")
    else:
        print("Неверный формат темы:", topic_parts)

def subscribe_topics(client):
    client.subscribe("device_esp/#")
    client.on_message = on_message

def connect_and_subscribe():
    try:
        mqtt_connection_settings = MQTTConnection.objects.first()
        mqtt_broker = mqtt_connection_settings.mqtt_broker
        mqtt_port = mqtt_connection_settings.mqtt_port
        mqtt_username = mqtt_connection_settings.mqtt_username
        mqtt_password = mqtt_connection_settings.mqtt_password

        client = mqtt.Client("mqtt_subscriber")
        client.username_pw_set(username=mqtt_username, password=mqtt_password)

        client.connect(mqtt_broker, mqtt_port, keep_alive)
        client.loop_start()

        print(f"Подключено к брокеру MQTT по адресу {mqtt_broker}:{mqtt_port} от имени пользователя {mqtt_username}")

        subscribe_topics(client)

        return client
    except Exception as e:
        print(f"Ошибка: {e}")

import signal

def exit_gracefully(signum, frame):
    print("Закрываем соединение с брокером.")
    mqtt_client.disconnect()
    exit(0)

if __name__ == "__main__":
    mqtt_client = connect_and_subscribe()

    # Настройте обработчик сигнала для graceful shutdown
    signal.signal(signal.SIGINT, exit_gracefully)

    # Дожидаемся сигнала остановки
    signal.pause()

""" if __name__ == "__main__":
    mqtt_client = connect_and_subscribe()

    # Дождитесь ввода пользователя для выхода
    input("Нажмите Enter, чтобы выйти...\n")

    print("Закрываем соединение с брокером.")
    mqtt_client.disconnect()  """