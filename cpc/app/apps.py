from django.apps import AppConfig


class CpcAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cpc.app"

    def ready(self):
        super().ready()
