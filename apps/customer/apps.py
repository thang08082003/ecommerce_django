

from django.apps import AppConfig
import importlib

class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customer'

    def ready(self):
        importlib.import_module('apps.customer.signals')  
