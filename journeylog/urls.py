from django.urls import path
from .views import JourneyLogView

urlpatterns = [
    path('', JourneyLogView.as_view(), name='journeylog'),
    path('get_data/<int:device_id>/', JourneyLogView.get_data, name='get_data'),
]
