from django.urls import path
from .views import DeviceAndMQTTConnectionView, DeviceUpdateView, DeviceDeleteView

urlpatterns = [
    path('', DeviceAndMQTTConnectionView.as_view(), name='device-view'),
    path('<int:device_id>/edit/', DeviceUpdateView.as_view(), name='device-edit'),
    path('<int:device_id>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
]
