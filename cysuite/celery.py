import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

DEBUG = bool(int(os.environ.get("DEBUG", 0)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cysuite.settings')
app = Celery('cysuite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()