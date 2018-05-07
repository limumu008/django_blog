from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path(r'create_order/', views.create_order, name='create_order'),
    path(r'payment/', views.payment_process, name='payment_process'),
    # 其他地方用
    path(r'payment/<int:order_id>/', views.payment_process, name='payment_process_0'),
    path(r'pay_done/', views.payment_done, name='pay_done'),
    path(r'pay_canceled/', views.payment_canceled, name='pay_canceled'),
    path(r'order_paid/<str:username>/', views.OrderPaidView.as_view(), name='orders_paid'),
    path(r'order_not_paid/<str:username>/', views.OrderNotPaidView.as_view(), name='orders_not_paid'),
]
