from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
    UserCreationForm
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    """用于注册用户"""
    error_messages = {
        'password_mismatch': _("密码不匹配"),
        'email_exists': _("邮箱已注册"),
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        all_user = get_user_model().objects.all()
        for user in all_user:
            if email != user.email:
                pass
            else:
                raise forms.ValidationError(
                        self.error_messages['email_exists'],
                        code='email_exists',
                )
        else:
            return email

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def send_link(self, user=None, domain_override=None,
                  subject_template_name='registration/activate_subject.txt',
                  email_template_name='registration/activate_email.html',
                  use_https=False, token_generator=default_token_generator,
                  from_email=None, request=None, html_email_template_name=None,
                  extra_email_context=None):
        email = self.cleaned_data['email']
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            'email': email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        if extra_email_context is not None:
            context.update(extra_email_context)
        self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
        )


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
        'password_mismatch': _("两次新密码不匹配"),
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
