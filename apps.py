from django.apps import AppConfig


class TotalConfig(AppConfig):
    name = 'total'

def ready(self):
    import total.signals
