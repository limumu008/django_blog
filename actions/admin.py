from django.contrib import admin

from actions.models import Action


class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('user', 'verb')


admin.site.register(Action, ActionAdmin)
