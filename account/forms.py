from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
    UserCreationForm
)

from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    """用于注册用户"""
    error_messages = {
        'password_mismatch': _("密码不匹配"),
    }

    email = forms.EmailField(max_length=50, required=True, label='邮箱',
                             help_text='用于重置密码等')
    password1 = forms.CharField(
            label=_("密码"),
            strip=False,
            widget=forms.PasswordInput,
            help_text='不能少于8位，不能只是数字，不能与用户名相同'
    )
    password2 = forms.CharField(
            label=_("重复密码"),
            widget=forms.PasswordInput,
            strip=False,
            help_text=_(
                    "再次输入密码"),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", 'email', 'password1', 'password2')
        labels = {
            'username': '用户名'
        }
        help_texts = {'username': ''}


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        help_texts = {'username': ''}
        labels = {
            'username': '用户名',
            'email': '邮箱'
        }


class ResetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("两次密码不相同"),
    }
    new_password1 = forms.CharField(
            label=_("新密码"),
            widget=forms.PasswordInput,
            strip=False,
            help_text='至少8位，与旧密码不同，不能全是数字',
    )
    new_password2 = forms.CharField(
            label=_("新密码确认"),
            strip=False,
            widget=forms.PasswordInput,
    )


class PasswordChangeForm0(PasswordChangeForm):
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("旧密码输入错误，请重新输入。"),
    })
    old_password = forms.CharField(
            label=_("旧密码"),
            strip=False,
            widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
    new_password1 = forms.CharField(
            label=_("新密码"),
            widget=forms.PasswordInput,
            strip=False,
            help_text='至少8位，与旧密码不同，不能全是数字',
    )
    new_password2 = forms.CharField(
            label=_("新密码确认"),
            strip=False,
            widget=forms.PasswordInput,
    )
