import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

app = Celery('online_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'catalog.tasks.some_scheduled_task',
        'schedule': 10
    },
    'check_orders': {
        'task': 'catalog.tasks.check_orders_and_send_email',
        'schedule': crontab(minute='*/1')
    }
}
