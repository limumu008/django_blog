from django import template
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from blog.models import Article, Likes

register = template.Library()


@register.filter(name='markdown_format')
def markdown_format(value):
    """使 markdown 文档正常展示"""
    return mark_safe(markdownify(value))


@register.filter(name='is_liked')
def is_liked(value, user):
    """
    测试 user 是否赞了 article/comment/reply
    :param value: have to be article/comment/reply
    :param user: have to be user
    :rtype: bool，表示评论是否被赞
    """
    if isinstance(user, AnonymousUser):
        return False
    try:
        content_type = ContentType.objects.get_for_model(value)
        like = Likes.objects.get(user=user,
                                 content_type=content_type,
                                 object_id=value.id)
        is_liked_0 = like.is_liked
        return is_liked_0
    except Likes.DoesNotExist:
        return False


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


@register.simple_tag(name='count_likes')
def count_likes(target):
    """获取 article/comment/reply 赞数
    :param target:have to be article/comment/reply
    :return: pos int
    """
    try:
        content_type = ContentType.objects.get_for_model(target)
        likes = Likes.objects.filter(content_type=content_type,
                                     object_id=target.id,
                                     is_liked=True
                                     ).count()
        return likes
    except Likes.DoesNotExist:
        return 0
