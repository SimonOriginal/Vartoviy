# urls.py
from django.urls import path
from .views import NotificationsView, UnviewedNotificationsCountView

urlpatterns = [
    path('', NotificationsView.as_view(), name='notifications'),
    path('unviewed_notifications_count/', UnviewedNotificationsCountView.as_view(), name='unviewed_notifications_count'),
]
