from django.apps import AppConfig


class ClienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cliente'

    def ready(self):
        from django.db.models.signals import pre_save
        from .models import Cliente
        from .signals import created_user_client