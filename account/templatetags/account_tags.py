from django import template

register = template.Library()


@register.simple_tag(name='user_fans')
def user_fans(user):
    """user的粉丝数"""
    return user.fan0.count()


@register.simple_tag(name='user_stars')
def user_stars(user):
    """user的关注的人数"""
    return user.star0.count()
