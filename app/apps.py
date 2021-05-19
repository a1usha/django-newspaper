from django.apps import AppConfig

class AuthorizationConfig(AppConfig):
    name = "app"

    def ready(self) -> None:
        import app.signals