web: gunicorn cysuite.wsgi
worker: celery -A cysuite worker -P threads -l info --without-gossip --without-mingle