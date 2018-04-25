from django.contrib.contenttypes.models import ContentType

from actions.utils import create_action
from .models import Likes, Article, Comment, Reply


def create_like(user, target):
    """创建并保存 点赞 article/comment/reply like 的快捷函数"""
    try:
        # 尝试获取赞的目标对象
        content_type = ContentType.objects.get_for_model(target)
        like = Likes.objects.get(user=user,
                                 content_type=content_type,
                                 object_id=target.id)
        like.is_liked = not like.is_liked
        # target is article
        if isinstance(target, Article):
            if like.is_liked:
                create_action(user, target,
                              verb=f"{user.username} 赞了文章《{target.title}》")
            else:
                create_action(user, target,
                              verb=f"{user.username} 取消了文章《{target.title}》的赞")

        # target is comment
        elif isinstance(target, Comment):
            if like.is_liked:
                create_action(user, target,
                              verb=f"{user.username} 赞了评论:{target.content[:20]}")
            else:
                create_action(user, target,
                              verb=f"{user.username} 取消了评论:{target.content[:20]}的赞")
        # target is reply
        elif isinstance(target, Reply):
            if like.is_liked:
                create_action(user, target,
                              verb=f"{user.username} 赞了回复:{target.content[:20]}")
            else:
                create_action(user, target,
                              verb=f"{user.username} 取消了回复:{target.content[:20]}的赞")
        like.save()
    except Likes.DoesNotExist as e:
        like = Likes(user=user, likes_target=target)
        like.save()
        # target is article
        if isinstance(target, Article):
            create_action(user, target,
                          verb=f"{user.username}赞了文章《{target.title}》")
        # target is comment
        elif isinstance(target, Comment):
            create_action(user, target,
                          verb=f"{user.username}赞了评论:{target.content[:20]}")
        # target is reply
        elif isinstance(target, Reply):
            create_action(user, target,
                          verb=f"{user.username}赞了回复:{target.content[:20]}")
    return like


def toggle_pages(page_list, per_page_numbers=10):
    """接收准备分页的对象列表，返回是否为空的布尔值"""
    if page_list:
        page_toggle = True
        if page_list.count() <= per_page_numbers:
            page_toggle = False
    else:
        page_toggle = False
    return page_toggle
