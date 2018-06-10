from django.apps import apps
from django.forms import modelform_factory


def get_model(model_name):
    """ 获取 content 的 model class：model_name get from url"""
    if model_name in ('text', 'file', 'image'):
        return apps.get_model('courses', model_name)
    else:
        return None


def get_modelform(model):
    return modelform_factory(model, exclude=('owner', 'created', 'updated'))
