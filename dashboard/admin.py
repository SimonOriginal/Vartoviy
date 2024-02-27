from django.contrib import admin
from .models import Device, DeviceInfo, DeviceMeasurements

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'device_name', 'user')
    list_filter = ('user',)
    search_fields = ('unit_number', 'device_name')

@admin.register(DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('device', 'battery_charge', 'satellite_count', 'latitude', 'longitude', 'inside_or_not', 'date_time')
    list_filter = ('device__user',)
    search_fields = ('device__unit_number', 'device__device_name', 'date_time')

@admin.register(DeviceMeasurements)
class DeviceMeasurementsAdmin(admin.ModelAdmin):
    list_display = ('measurement_id', 'device', 'cumulative_angle', 'pressure', 'altitude', 'temperature', 'humidity', 'taser_activations', 'date_time')
    list_filter = ('device__user',)
    search_fields = ('device__unit_number', 'device__device_name', 'date_time')
