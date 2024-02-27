from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from dashboard.models import DeviceInfo, Device, DeviceMeasurements
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeviceInfoListView(View):
    template_name = 'tables/tables_info_device.html'

    def get(self, request, *args, **kwargs):
        devices = Device.objects.filter(user=request.user)
        context = {'devices': devices}
        return render(request, self.template_name, context)

from django.db.models import F

class DeviceDataView(View):
    def get(self, request, *args, **kwargs):
        device_id = request.GET.get('device_id')

        device_info_list = DeviceInfo.objects.filter(device_id=device_id).order_by('-date_time')
        device_measurements_list = DeviceMeasurements.objects.filter(device_id=device_id).order_by('-date_time')

        paginator_info = Paginator(device_info_list, 25)
        paginator_measurements = Paginator(device_measurements_list, 25)

        page_info = request.GET.get('page_info', 1)
        page_measurements = request.GET.get('page_measurements', 1)

        try:
            device_info_page = paginator_info.page(page_info)
        except PageNotAnInteger:
            device_info_page = paginator_info.page(1)
        except EmptyPage:
            device_info_page = paginator_info.page(paginator_info.num_pages)

        try:
            device_measurements_page = paginator_measurements.page(page_measurements)
        except PageNotAnInteger:
            device_measurements_page = paginator_measurements.page(1)
        except EmptyPage:
            device_measurements_page = paginator_measurements.page(paginator_measurements.num_pages)

        data = {
            'current_page_info': device_info_page.number,
            'total_pages_info': paginator_info.num_pages,
            'device_info': [
                {
                    'battery_charge': info.battery_charge,
                    'satellite_count': info.satellite_count,
                    'latitude': info.latitude,
                    'longitude': info.longitude,
                    'inside_or_not': info.inside_or_not,
                    'date_time': info.date_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for info in device_info_page
            ],
            'current_page_measurements': device_measurements_page.number,
            'total_pages_measurements': paginator_measurements.num_pages,
            'device_measurements': [
                {
                    'measurement_id': measurement.measurement_id,
                    'cumulative_angle': measurement.cumulative_angle,
                    'pressure': measurement.pressure,
                    'altitude': measurement.altitude,
                    'temperature': measurement.temperature,
                    'humidity': measurement.humidity,
                    'taser_activations': measurement.taser_activations,
                    'date_time': measurement.date_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for measurement in device_measurements_page
            ]
        }

        return JsonResponse(data, safe=False)

""" class DeviceDataView(View): "копия рабочая без сортировки по дате новый старый отобрвжение "

    def get(self, request, *args, **kwargs):
        device_id = request.GET.get('device_id')

        device_info_list = DeviceInfo.objects.filter(device_id=device_id)
        device_measurements_list = DeviceMeasurements.objects.filter(device_id=device_id)
        # Измени число "25" если нужно больше записей на одной странице

        paginator_info = Paginator(device_info_list, 25)
        paginator_measurements = Paginator(device_measurements_list, 25)


        page_info = request.GET.get('page_info', 1)
        page_measurements = request.GET.get('page_measurements', 1)

        try:
            device_info_page = paginator_info.page(page_info)
        except PageNotAnInteger:
            device_info_page = paginator_info.page(1)
        except EmptyPage:
            device_info_page = paginator_info.page(paginator_info.num_pages)

        try:
            device_measurements_page = paginator_measurements.page(page_measurements)
        except PageNotAnInteger:
            device_measurements_page = paginator_measurements.page(1)
        except EmptyPage:
            device_measurements_page = paginator_measurements.page(paginator_measurements.num_pages)

        data = {
            'current_page_info': device_info_page.number,
            'total_pages_info': paginator_info.num_pages,
            'device_info': [
                {
                    'battery_charge': info.battery_charge,
                    'satellite_count': info.satellite_count,
                    'latitude': info.latitude,
                    'longitude': info.longitude,
                    'inside_or_not': info.inside_or_not,
                    'date_time': info.date_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for info in device_info_page
            ],
            'current_page_measurements': device_measurements_page.number,
            'total_pages_measurements': paginator_measurements.num_pages,
            'device_measurements': [
                {
                    'measurement_id': measurement.measurement_id,
                    'cumulative_angle': measurement.cumulative_angle,
                    'pressure': measurement.pressure,
                    'altitude': measurement.altitude,
                    'temperature': measurement.temperature,
                    'humidity': measurement.humidity,
                    'taser_activations': measurement.taser_activations,
                    'date_time': measurement.date_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for measurement in device_measurements_page
            ]
        }

        return JsonResponse(data, safe=False) """