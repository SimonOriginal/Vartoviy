from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('device', 'message', 'timestamp')
    list_filter = ('device', 'timestamp')
    search_fields = ('device__name', 'message')
    date_hierarchy = 'timestamp'

admin.site.register(Notification, NotificationAdmin)
