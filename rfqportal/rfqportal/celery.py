import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfqportal.settings')

# Create a Celery instance
celery_app = Celery('rfqportal')
# Load task modules from all registered Django app configs
celery_app.autodiscover_tasks()
# Set the timezone for Celery           
celery_app.conf.timezone = 'UTC'
# Set the task serializer to JSON
celery_app.conf.task_serializer = 'json'
celery_app.config_from_object('django.conf:settings', namespace='CELERY')