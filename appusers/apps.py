from django.apps import AppConfig


class AppusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appusers'
    
    def ready(self):
        import appusers.signals
