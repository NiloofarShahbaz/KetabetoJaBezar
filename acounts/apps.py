from django.apps import AppConfig


class AcountsConfig(AppConfig):
    name = 'acounts'

    def ready(self):
        import acounts.signals
