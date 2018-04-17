from .models import Action


def create_action(user, target, verb):
    """创建并保存 action实例的快捷函数"""
    action = Action(user=user, verb=verb, target=target)
    action.save()
