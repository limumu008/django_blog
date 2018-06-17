from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from django_blog import settings
from order.models import Order


def payment_notice(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            return None
        else:
            order = get_object_or_404(Order, id=ipn_obj.invoice)
            order.is_paid = True
            order.save()


valid_ipn_received.connect(payment_notice)
