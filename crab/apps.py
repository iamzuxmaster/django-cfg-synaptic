from django.apps import AppConfig


class CrabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crab'

    def ready(self):
            import crab.signals