from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from blog.models import Article, Likes

register = template.Library()


@register.filter(name='markdown_format')
def markdown_format(value):
    """使 markdown 文档正常展示"""
    return mark_safe(markdownify(value))


@register.simple_tag(name='article_counts')
def article_counts(user):
    """撰写的文章总数"""
    return Article.published.filter(author=user).count()


@register.simple_tag(name='draft_counts')
def draft_counts(user):
    """获取用户撰写的草稿总数"""
    return Article.objects.filter(author=user).filter(status='draft').count()


@register.simple_tag(name='comments_counts')
def comments_counts(article):
    """获取文章评论总数"""
    return article.comments.all().count()


@register.simple_tag(name='article_likes')
def article_likes(article):
    """获取文章赞数"""
    try:
        content_type = ContentType.objects.get_for_model(article)
        likes = Likes.objects.filter(content_type=content_type,
                                     object_id=article.id,
                                     is_liked=True
                                     ).count()
        return likes
    except Exception:
        return 0
