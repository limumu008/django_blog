from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'publish', 'status', 'content']
    list_filter = ['author', 'publish', 'status']
    search_fields = ['title', 'content']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Article, ArticleAdmin)
