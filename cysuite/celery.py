import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cysuite.settings')
app = Celery('cysuite')
app.autodiscover_tasks()