from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dashboard.models import Device
from .models import MQTTConnection
from .forms import MQTTConnectionForm

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeviceAndMQTTConnectionView(View):
    template_name = 'device_aud/device_aud.html'

    def get(self, request):
        try:
            connection = MQTTConnection.objects.get()
        except MQTTConnection.DoesNotExist:
            connection = None

        user_devices = Device.objects.filter(user=request.user)
        return render(request, self.template_name, {'devices': user_devices, 'connection': connection, 'form_id': 'mqtt_connection_form'})

    def post(self, request):
        unit_number = request.POST.get('unit_number')
        device_name = request.POST.get('device_name')
        mqtt_broker = request.POST.get('mqtt_broker')
        mqtt_port = request.POST.get('mqtt_port')
        mqtt_username = request.POST.get('mqtt_username')
        mqtt_password = request.POST.get('mqtt_password')

        # Проверка наличия unit_number перед преобразованием в int
        if unit_number is not None:
            try:
                unit_number = int(unit_number)
            except ValueError:
                user_devices = Device.objects.filter(user=request.user)
                error_message = "Идентификатор устройства должен быть числом."
                return render(request, self.template_name, {'devices': user_devices, 'error_message': error_message})

        # Проверка наличия mqtt_port, mqtt_broker и других полей перед созданием объекта MQTTConnection
        if mqtt_port is not None and mqtt_broker is not None:
            try:
                connection = MQTTConnection.objects.get()
                connection.mqtt_broker = mqtt_broker
                connection.mqtt_port = mqtt_port
                connection.mqtt_username = mqtt_username
                connection.mqtt_password = mqtt_password
                connection.save()
            except MQTTConnection.DoesNotExist:
                MQTTConnection.objects.create(
                    mqtt_broker=mqtt_broker,
                    mqtt_port=mqtt_port,
                    mqtt_username=mqtt_username,
                    mqtt_password=mqtt_password
                )

        # Проверка наличия unit_number и device_name перед созданием объекта Device
        if unit_number is not None and device_name:
            # Проверка наличия объекта с таким unit_number
            if Device.objects.filter(unit_number=unit_number).exists():
                user_devices = Device.objects.filter(user=request.user)
                error_message = f"Устройство с номером {unit_number} уже существует."
                return render(request, self.template_name, {'devices': user_devices, 'error_message': error_message})
            
            Device.objects.create(unit_number=unit_number, device_name=device_name, user=request.user)

        # После успешного создания устройства или обновления параметров MQTT,
        # перенаправляем на страницу с устройствами
        return redirect('device-view')  # Имя вашего URL-шаблона

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeviceUpdateView(View):
    template_name = 'device_aud/device_aud.html'

    def get(self, request, device_id):
        device = Device.objects.get(pk=device_id, user=request.user)
        return render(request, self.template_name, {'device': device})

    def post(self, request, device_id):
        device = Device.objects.get(pk=device_id, user=request.user)

        unit_number = request.POST.get('unit_number')
        device_name = request.POST.get('device_name')

        try:
            unit_number = int(unit_number)
        except ValueError:
            user_devices = Device.objects.filter(user=request.user)
            error_message = "Идентификатор устройства должен быть числом."
            return render(request, self.template_name, {'devices': user_devices, 'error_message': error_message})

        # Проверка наличия объекта с таким unit_number, исключая текущий объект
        if Device.objects.filter(unit_number=unit_number).exclude(pk=device_id).exists():
            user_devices = Device.objects.filter(user=request.user)
            error_message = f"Устройство с номером {unit_number} уже существует."
            return render(request, self.template_name, {'devices': user_devices, 'error_message': error_message})

        device.unit_number = unit_number
        device.device_name = device_name
        device.save()

        # После успешного обновления устройства, перенаправляем на страницу с устройствами
        return redirect('device-view')

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeviceDeleteView(View):
    template_name = 'device_aud/device_aud.html'

    def get(self, request, device_id):
        try:
            device = Device.objects.get(pk=device_id, user=request.user)
            device.delete()
        except Device.DoesNotExist:
            user_devices = Device.objects.filter(user=request.user)
            error_message = "Устройство не существует или не принадлежит вам."
            return render(request, self.template_name, {'devices': user_devices, 'error_message': error_message})

        # После успешного удаления устройства, перенаправляем на страницу с устройствами
        return redirect('device-view')  # Замените 'device_list' на имя вашего URL-

""" # Добавление и редактирование параметров MQTT
class MQTTConnectionView(View):
    template_name = 'device_aud/device_aud.html'

    def get(self, request):
        try:
            connection = MQTTConnection.objects.get()
        except MQTTConnection.DoesNotExist:
            connection = None

        return render(request, self.template_name, {'connection': connection, 'form_id': 'mqtt_connection_form'})

    def post(self, request):
        mqtt_broker = request.POST.get('mqtt_broker')
        mqtt_port = request.POST.get('mqtt_port')
        mqtt_username = request.POST.get('mqtt_username')
        mqtt_password = request.POST.get('mqtt_password')

        try:
            connection = MQTTConnection.objects.get()
            connection.mqtt_broker = mqtt_broker
            connection.mqtt_port = mqtt_port
            connection.mqtt_username = mqtt_username
            connection.mqtt_password = mqtt_password
            connection.save()
        except MQTTConnection.DoesNotExist:
            MQTTConnection.objects.create(
                mqtt_broker=mqtt_broker,
                mqtt_port=mqtt_port,
                mqtt_username=mqtt_username,
                mqtt_password=mqtt_password
            )

        return redirect('mqtt_connection') """