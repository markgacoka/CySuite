web: gunicorn cysuite.wsgi
celery: celery -A cysuite worker -P threads -l INFO --concurrency=8