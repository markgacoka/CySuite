import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

DEBUG = bool(int(os.environ.get("DEBUG", 0)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cysuite.settings')
if DEBUG:
    app = Celery('cysuite', backend='redis', broker=os.environ.get('CELERY_BROKER_URL'))
else:
    app = Celery('cysuite', backend='redis', broker=os.environ.get('REDISTOGO_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()