from django.urls import path
from .views import DeviceInfoListView, DeviceDataView

urlpatterns = [
    path('', DeviceInfoListView.as_view(), name='tables'),
    path('device_data/', DeviceDataView.as_view(), name='device_data'),
    # Другие пути к представлениям могут быть добавлены здесь
]
