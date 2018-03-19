from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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
