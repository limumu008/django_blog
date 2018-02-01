from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'author', 'publish', 'status', 'content']


admin.site.register(Article, ArticleAdmin)
