from django.shortcuts import redirect, render
from .models import Device, DeviceMeasurements, DeviceInfo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json

@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeView(View):
    def get(self, request):
        # Фильтруем устройства по текущему пользователю
        devices = Device.objects.filter(user_id=request.user.id)
        return render(request, 'home/home.html', {'devices': devices})

class UpdateDeviceInfoView(View):
    def post(self, request):
        device_id = request.POST.get('device_id')

        # Получение последней информации об устройстве
        device_info = DeviceInfo.objects.filter(device_id=device_id).order_by('-date_time').first()

        # Получайте данные о последних измерениях устройств
        device_measurements = DeviceMeasurements.objects.filter(device_id=device_id).order_by('-date_time')

        info_data = {
            'battery_charge': device_info.battery_charge,
            'satellite_count': device_info.satellite_count,
            'latitude': device_info.latitude,
            'longitude': device_info.longitude,
            'inside_or_not': device_info.inside_or_not,
            'date_time': device_info.date_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        measurements_data = []
        for measurement in device_measurements:
            measurement_data = {
                'cumulative_angle': measurement.cumulative_angle,
                'pressure': measurement.pressure,
                'altitude': measurement.altitude,
                'temperature': measurement.temperature,
                'humidity': measurement.humidity,
                'taser_activations': measurement.taser_activations,
                'date_time': measurement.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            measurements_data.append(measurement_data)

        response_data = {'info': info_data, 'measurements': measurements_data}

        return JsonResponse(response_data)
    
class DeviceDataView(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        device_id = data.get('device_id')
        
        # Фильтрация данных из модели DeviceInfo
        device_info_records = DeviceInfo.objects.filter(device_id=device_id)

        # Фильтрация данных из модели DeviceMeasurements
        device_measurements = DeviceMeasurements.objects.filter(device_id=device_id)

        # Aggregate values from multiple DeviceInfo records if there are more than one
        battery_charge_values = [info.battery_charge if info is not None else 0.0 for info in device_info_records]
        satellite_count_values = [info.satellite_count if info is not None else 0 for info in device_info_records]
        inside_or_not_values = [info.inside_or_not if info is not None else False for info in device_info_records]
        labels = [info.date_time.strftime('%Y-%m-%d %H:%M:%S') for info in device_info_records]
        
        data = {
            'labels': labels,
            'battery_charge': battery_charge_values,
            'satellite_count': satellite_count_values,
            'inside_or_not': inside_or_not_values,
            'cumulative_angle': [measurement.cumulative_angle for measurement in device_measurements],
            'pressure': [measurement.pressure for measurement in device_measurements],
            'altitude': [measurement.altitude for measurement in device_measurements],
            'temperature': [measurement.temperature for measurement in device_measurements],
            'humidity': [measurement.humidity for measurement in device_measurements],
            'taser_activations': [measurement.taser_activations for measurement in device_measurements],
        }
        
        return JsonResponse(data)

class PointView(View):
    def post(self, request):
        device_id = request.POST.get('device_id')
        
        # Получение последней информации об устройстве
        device_info = DeviceInfo.objects.filter(device_id=device_id).order_by('-date_time').first()
        
        # Проверка, что объект device_info не является None
        if device_info is not None:
            info_data = {
                'latitude': device_info.latitude,
                'longitude': device_info.longitude,
                'date_time': device_info.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        else:
            # Обработка случая, когда device_info равен None
            info_data = {
                'latitude': 0.0,
                'longitude': 0.0,
                'date_time': 'N/A',
            }

        response_data = {'info': info_data}
        return JsonResponse(response_data)

""" from django.urls import reverse
from django.views import View
from django.shortcuts import redirect
from django.utils.translation import activate

class SetLanguageView(View):
    def get(self, request, language, *args, **kwargs):
        # Set the language
        activate(language)
        request.session['language'] = language

        # Get the referer (previous page) or use a default URL
        referer = request.META.get('HTTP_REFERER', reverse('home'))

        # Redirect back to the referer
        return redirect(referer) """

