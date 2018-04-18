from django.contrib import admin

from .models import Article, Comment, Likes


class CommentInline(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'publish', 'status', 'content', 'tags']
    list_filter = ['author', 'publish', 'status']
    search_fields = ['title', 'content']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    inlines = [CommentInline]


class LikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'is_liked')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Likes, LikesAdmin)
