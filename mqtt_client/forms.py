from django import forms
from dashboard.models import Device
from .models import MQTTConnection

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['unit_number', 'device_name']

class MQTTConnectionForm(forms.ModelForm):
    class Meta:
        model = MQTTConnection
        fields = ['mqtt_broker', 'mqtt_port', 'mqtt_username', 'mqtt_password']
