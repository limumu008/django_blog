from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_blog import settings


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
            _('username'),
            max_length=150,
            unique=True,
            validators=[username_validator],
            error_messages={
                'unique': _("用户已注册"),
            },
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"{self.user.username} profile"
