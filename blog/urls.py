from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'article/<int:pk>/', views.ArticleView.as_view(), name='articles'),
    path(r'share_article/<int:id>/', views.share_article, name='share_article'),

]
