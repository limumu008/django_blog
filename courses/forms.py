from django.forms import inlineformset_factory

from .models import Course, Module

ModuleFormSet = inlineformset_factory(Course, Module,
                                      fields=('title', 'description'),
                                      extra=2,
                                      can_delete=True, labels={'title': '标题', 'description': '描述'})
