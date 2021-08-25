from celery import shared_task
from time import sleep

@shared_task(bind=True)
def go_to_sleep(self, duration):
    sleep(duration)
    return 'Done'