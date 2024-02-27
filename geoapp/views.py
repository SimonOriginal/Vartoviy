from django.shortcuts import get_object_or_404, render
from django.views import View
from dashboard.models import Device
from .models import GeoZone
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


@method_decorator(login_required(login_url='login'), name='dispatch')
class ConfigurationView(LoginRequiredMixin, View):
    def get(self, request):
        # Получаем геозоны, связанные с текущим пользователем
        geo_zones = GeoZone.objects.filter(user=request.user)
        # Получаем устройства текущего пользователя
        devices = Device.objects.filter(user=request.user)
        return render(request, 'geomaps/virtual_barrier.html', {'geo_zones': geo_zones, 'devices': devices})

def save_geozone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        geojson = data.get('geojson')
        name = data.get('name')
        device_id = data.get('device_id')

        # Убедитесь, что устройство существует и принадлежит текущему пользователю
        device = Device.objects.get(id=device_id, user=request.user)

        # Создание или обновление геозоны, связанной с указанным устройством
        geozone, created = GeoZone.objects.get_or_create(user=request.user, device=device)
        geozone.geojson = geojson
        geozone.name = name
        geozone.save()

        return JsonResponse({'message': 'Геозона успешно сохранена в базу данных!'})
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)


def get_geojson(request):
    # Получаем значение device_id из POST-запроса
    device_id = request.POST.get('device_id')
    print(f"Device ID: {device_id}")
    # Проверяем, связано ли устройство с текущим пользователем
    device = get_object_or_404(Device, id=device_id, user=request.user)

    # Получаем геозону, связанную с устройством
    try:
        geozone = GeoZone.objects.get(user=request.user, device=device)
        geojson_data = geozone.geojson
        return JsonResponse({'geojson': geojson_data})
        
    except GeoZone.DoesNotExist:
        return JsonResponse({'error': 'Геозона не найдена для указанного устройства'}, status=404)


""" # Функция для отображения страницы с картой
@method_decorator(login_required(login_url='login'), name='dispatch')
def configuration(request):
    return render(request, 'geomaps/virtual_barrier.html') """

""" @method_decorator(login_required(login_url='login'), name='dispatch')
class ConfigurationView(View):
    def get(self, request):
        return render(request, 'geomaps/virtual_barrier.html')
    
@csrf_exempt
def save_geozone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        geojson = data.get('geojson')
        name = data.get('name')

        # Проверяем, существует ли уже запись в базе данных
        try:
            geozone = GeoZone.objects.get()
            # Если запись существует, обновляем ее поля данными из нового запроса
            geozone.geojson = geojson
            geozone.name = name
        except GeoZone.DoesNotExist:
            # Если записи нет, создаем новую запись
            geozone = GeoZone(geojson=geojson, name=name)
        # Сохраняем или обновляем запись в базе данных
        geozone.save()

        # Возвращаем JSON-ответ об успешном сохранении или обновлении
        return JsonResponse({'message': 'Геозона успешно сохранена в базу данных!'})
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    

def get_geojson(request):
    # Получаем последнюю запись из базы данных
    try:
        geozone = GeoZone.objects.latest('created_at')
        geojson_data = geozone.geojson
        return JsonResponse({'geojson': geojson_data})
    except GeoZone.DoesNotExist:
        return JsonResponse({'error': 'Геозона не найдена'}, status=404) """


"""
# Это для сохранения множества зон в базу данных
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt  # Разрешаем запросы без CSRF токена (для упрощения примера)
def save_geozone(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        data = json.loads(request.body)
        geojson = data.get('geojson')
        name = data.get('name')
        
        # Создаем новый объект GeoZone и сохраняем его в базу данных
        geozone = GeoZone(geojson=geojson, name=name)
        geozone.save()
        
        # Возвращаем JSON-ответ об успешном сохранении
        return JsonResponse({'message': 'Геозона успешно сохранена в базу данных!'})
    else:
        # Возвращаем JSON-ответ об ошибке метода запроса
        return JsonResponse({'error': 'Метод не разрешен'}, status=405) """
