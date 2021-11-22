from django.apps import AppConfig


class CyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cyauth'

    def ready(self):
        import cyauth.signals
