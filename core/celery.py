import os
from celery import Celery

# Setting the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Reading config from settings.py using namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Loading tasks from all registered apps
app.autodiscover_tasks()