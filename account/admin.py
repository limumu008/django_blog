from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_author']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
