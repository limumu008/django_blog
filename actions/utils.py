from .models import Action


def create_action(user, target, verb):
    """创建并保存 action实例的快捷函数"""
    try:
        action = Action.objects.get(user=user, verb=verb)
        action.save(update_fields=['updated'])
    except Action.DoesNotExist as e:
        action = Action(user=user, verb=verb, target=target)
        action.save()
