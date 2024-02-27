from django.urls import path
from . import views
from .views import HomeView, UpdateDeviceInfoView, DeviceDataView, PointView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('update_device_info/', UpdateDeviceInfoView.as_view(), name='update_device_info'),
    path('charts/', DeviceDataView.as_view(), name='charts'),
    path('point/', PointView.as_view(), name='point'),
    # ... other URL patterns ...
]
