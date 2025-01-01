from django.apps import AppConfig


class AppgilloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appGillo'

    def ready(self):
        import appGillo.signals
