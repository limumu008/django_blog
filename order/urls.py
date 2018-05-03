from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    # path(r'create_order/', views.OrderCreateView.as_view(), name='create_order'),
    path(r'create_order/', views.create_order, name='create_order'),
]
