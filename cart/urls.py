from django.urls import path

from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('change_cart/', views.change_cart, name='change_cart'),
]
