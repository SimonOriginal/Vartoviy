import paho.mqtt.client as mqtt
import json
import time
import random

# Настройки MQTT брокера
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_username = "hivemq"  # Замените на ваше имя пользователя MQTT
mqtt_password = "1307YDZASzByi;,uqv<&"  # Замените на ваш пароль MQTT

# Настройки виртуального датчика
device_id = 111111  # ID устройства в вашей базе данных
keep_alive = 60

temperature_celsius_topic = f"device_esp/{device_id}/temperatureCelsius"
temperature_fahrenheit_topic = f"device_esp/{device_id}/temperatureFahrenheit"
humidity_topic = f"device_esp/{device_id}/humidity"
pressure_topic = f"device_esp/{device_id}/pressure"
altitude_topic = f"device_esp/{device_id}/altitude"
battery_charge_topic = f"device_esp/{device_id}/battery_charge"
gps_topic = f"device_esp/{device_id}/gps"
zone_status_topic = f"device_esp/{device_id}/zone_status"
shocker_topic = f"device_esp/{device_id}/shocker"
satellite_count_topic = f"device_esp/{device_id}/satellite_count"

# Создание клиента MQTT с учетными данными
client = mqtt.Client("virtual_sensor")
client.username_pw_set(username=mqtt_username, password=mqtt_password)

# Функция для отправки данных на брокер
def publish_data():
    temperature_celsius = round(random.uniform(-10, 50), 2)
    temperature_fahrenheit = round((temperature_celsius * 9/5) + 32, 2)
    humidity = round(random.uniform(30, 70), 2)
    pressure = round(random.uniform(900, 1100), 2)
    altitude = round(random.uniform(0, 400), 2)
    battery_charge = round(random.uniform(0, 100), 2)
    satellite_count = round(random.uniform(0, 25), 0)
    in_zone = random.choice([True, False])
    shocker_activated = random.choice([True, False])
    latitude = round(random.uniform(51, 51), 3) + round(random.uniform(0.3671, 0.3779), 6)
    longitude = round(random.uniform(7, 7), 3) + round(random.uniform(0.5761, 0.5769), 6)
    gps_payload = (latitude, longitude)

    # Отправка данных с QoS 0
    client.publish(temperature_celsius_topic, json.dumps(temperature_celsius), qos=0)
    client.publish(temperature_fahrenheit_topic, json.dumps(temperature_fahrenheit), qos=0)
    client.publish(humidity_topic, json.dumps(humidity), qos=0)
    client.publish(pressure_topic, json.dumps(pressure), qos=0)
    client.publish(altitude_topic, json.dumps(altitude), qos=0)
    client.publish(battery_charge_topic, json.dumps(battery_charge), qos=0)
    client.publish(satellite_count_topic, json.dumps(satellite_count), qos=0)
    client.publish(gps_topic, json.dumps(gps_payload), qos=0)

    zone_status_payload = "1" if in_zone else "0"
    client.publish(zone_status_topic, zone_status_payload, qos=0)

    shocker_payload = "1" if shocker_activated else "0"
    client.publish(shocker_topic, shocker_payload, qos=0)

    print(f"Опубликованные данные: Температура по Цельсию: {temperature_celsius}, Температура по Фаренгейту: {temperature_fahrenheit}, Влажность: {humidity}, Давление: {pressure}, Высота: {altitude}, Заряд батареи: {battery_charge},In Zone: {in_zone}, Шокер: {shocker_payload}, GPS:{gps_payload}")

# Функция для подключения к брокеру и публикации данных
def connect_and_publish():
    try:
        client.connect(mqtt_broker, mqtt_port, keep_alive)
        client.loop_start()
        print("Подключился к брокеру MQTT. Публикует данные...")
        
        while True:
            try:
                publish_data()
                time.sleep(10)
            except Exception as e:
                print(f"Ошибка при публикации данных: {e}")
    except Exception as ex:
        print(f"Ошибка при подключении к брокеру MQTT: {ex}")

# Запуск виртуального датчика
if __name__ == "__main__":
    connect_and_publish()
