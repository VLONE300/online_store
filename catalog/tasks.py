from celery import shared_task
import time

from django.conf import settings

from catalog.models import Order
from datetime import timedelta
from django.core.mail import send_mail


@shared_task
def some_task():
    time.sleep(5)
    return 'fukk'


@shared_task
def some_scheduled_task():
    return 'OPP'


@shared_task()
def check_orders_and_send_email():
    orders = Order.objects.filter(payment_status='Paid')
    for order in orders:
        if not order.is_notif_sent:
            send_mail('Order from shop',
                      f'Your order {order.id} has been paid',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[order.user.email]
                      )

            order.is_notif_sent = True
            order.save()
