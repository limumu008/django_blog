from django.urls import path
from haystack.views import SearchView

from . import views

app_name = 'shop'

urlpatterns = [
    path(r'search/', SearchView(template='shop/search.html'), name='search_product'),
    path('', views.product_list, name='product_list'),
    path(r'<slug:category_slug>/', views.product_list, name='category_product_list'),
    path(r'product_detail/<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
