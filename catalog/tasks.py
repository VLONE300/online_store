from celery import shared_task
import time


@shared_task
def some_task():
    time.sleep(5)
    return 'fukk'
