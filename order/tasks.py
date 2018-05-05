from django.core.mail import send_mail

from django_blog.celery import app
from order.models import Order


@app.task
def order_created(order_id):
    """send mail,return the result:1/0"""
    order = Order.objects.get(id=order_id)
    subject = f"Order:{order_id}"
    message = f"亲爱的 {order.customer},\n\n你的订单（订单：{order_id}）已成功下达。"
    print(subject)
    print(message)
    mail_sent = send_mail(subject, message, 'wangzhou8284@163.com', [order.email])
    print(mail_sent)
    return mail_sent
