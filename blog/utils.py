from django.contrib.contenttypes.models import ContentType

from actions.utils import create_action
from .models import Article, Likes


def create_like_article(user, article):
    """创建并保存 点赞文章 like 实例的快捷函数"""
    try:
        # 尝试获取赞对象
        content_type = ContentType.objects.get_for_model(article)
        like = Likes.objects.get(user=user,
                                 content_type=content_type,
                                 object_id=article.id)
        like.is_liked = not like.is_liked
        if like.is_liked:
            create_action(user, article,
                          verb=f"{user.username}赞了文章《{article.title}》")
        else:
            create_action(user, article,
                          verb=f"{user.username} 取消了文章《{article.title}》的赞")
        like.save()
    except Likes.DoesNotExist as e:
        like = Likes(user=user, likes_target=article)
        like.save()
        create_action(user, article,
                      verb=f"{user.username}赞了文章《{article.title}》")
    return like