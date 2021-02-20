from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    name = 'helpdesk'

    def ready(self):
        import helpdesk.signals