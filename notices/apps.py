from django.apps import AppConfig


class NoticesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notices'
    verbose_name = 'Уведомления'
    
    def ready(self):
        import notices.signals
