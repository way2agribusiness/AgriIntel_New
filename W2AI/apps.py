from django.apps import AppConfig


class W2AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'W2AI'

    def ready(self):
        import W2AI.signals