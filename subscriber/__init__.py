import os

from celery import Celery
import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subscriber.settings')

# This is used when the service is run by Celery, as a worker.
celery = Celery('fitbit_subscriber')
celery.config_from_object(settings)
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
