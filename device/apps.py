from django.apps import AppConfig


class DeviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device'

    def ready(self) -> None:
        import device.signals
        return super().ready()
