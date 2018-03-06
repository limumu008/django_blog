from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'article/<int:pk>/', views.article_detail, name='articles'),
    path(r'share_article/<int:id>/', views.share_article, name='share_article'),
    path(r'tags/<slug:tag_slug>/', views.IndexView.as_view(), name='tag_index'),
    path(r'tags/', views.retrieve_tags, name='tags'),
]
