from django.urls import path

from . import views

app_name = 'coupon'
urlpatterns = [
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
]
