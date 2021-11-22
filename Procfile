web: gunicorn cysuite.wsgi
worker: celery -A cysuite worker -l info --without-gossip --without-mingle