from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'my_articles/', views.MyArticles.as_view(), name='my_articles'),
    path(r'my_articles/<slug:tag_slug>/', views.MyArticles.as_view(), name='my_articles_tags'),
    path(r'article/<int:pk>/', views.article_detail, name='articles'),
    path(r'share_article/<int:id>/', views.share_article, name='share_article'),
    path(r'tags/<slug:tag_slug>/', views.IndexView.as_view(), name='tag_index'),
    path(r'tags/', views.retrieve_tags, name='tags'),
    path(r'article/new/', views.NewArticle.as_view(), name='new_article'),
    path(r'article/update/<int:pk>/', views.UpdateArticle.as_view(), name='update_article'),
]
