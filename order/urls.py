from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path(r'create_order/', views.create_order, name='create_order'),
    path(r'payment/', views.payment_process, name='payment_process'),
    path(r'pay_done/', views.payment_done, name='pay_done'),
    path(r'pay_canceled/', views.payment_canceled, name='pay_canceled'),
]
