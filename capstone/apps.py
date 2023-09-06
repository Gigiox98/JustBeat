from django.apps import AppConfig
from django.conf import settings

class CapstoneConfig(AppConfig): # pragma: no cover
    name = 'capstone'

    def ready(self):
        from . import jobscheduler
        if settings.APSCHEDULER_AUTOSTART:
        	jobscheduler.start()
