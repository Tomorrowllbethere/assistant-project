from django.apps import AppConfig


class CloudConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'cloud'
    def ready(self):
        # Ось тут ми кажемо Django: "Коли будеш готовий, підключи наші сигнали"
        import cloud.signals