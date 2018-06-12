from django.urls import path
from django.views.decorators.cache import cache_page
from haystack.views import SearchView

from . import views

app_name = 'shop'

urlpatterns = [
    path(r'search/', SearchView(template='shop/search.html'), name='search_product'),
    path('', cache_page(60 * 15)(views.product_list), name='product_list'),
    path(r'<slug:category_slug>/', views.product_list, name='category_product_list'),
    path(r'product_detail/<int:pk>/<slug:slug>/', cache_page(60 * 15)(views.ProductDetailView.as_view()),
         name='product_detail'),
]
