# views.py
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from dashboard.models import DeviceInfo, Device

@method_decorator(login_required(login_url='login'), name='dispatch')
class JourneyLogView(LoginRequiredMixin, View):
    def get(self, request):
        devices = Device.objects.filter(user=request.user)  # Получать устройства только для вошедшего в систему пользователя
        return render(request, 'journeylog/journeylog.html', {'devices': devices})

    def get_data(request, device_id):
        # Убедитесь, что запрашиваемое устройство принадлежит вошедшему в систему пользователю
        device = Device.objects.get(id=device_id, user=request.user)
        data = DeviceInfo.objects.filter(device=device)
        points = [{'lat': d.latitude, 'lng': d.longitude, 'time': d.date_time.strftime('%Y-%m-%d %H:%M:%S')} for d in data]
        return JsonResponse(points, safe=False)
