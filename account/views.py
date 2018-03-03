from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView, \
    PasswordResetConfirmView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from account.forms import (
    PasswordChangeForm0,
    RegisterForm,
    ResetPasswordForm,
    UpdateUserForm)

User = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'activate_account'
INTERNAL_RESET_SESSION_TOKEN = '_activate_account_token'


@login_required
def account_profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


class RegisterView(generic.CreateView):
    # todo add email verification
    # todo add auto login
    model = User
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:register_done')

    from_email = None
    token_generator = default_token_generator
    email_template_name = 'registration/activate_email.html'
    subject_template_name = 'registration/activate_subject.txt'
    html_email_template_name = None
    extra_email_context = None

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def form_valid(self, form):
        """创建 is_active=False 的 user，然后发送激活链接到注册邮箱"""
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        opts = {
            'user': user,
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.send_link(**opts)
        return HttpResponseRedirect(self.get_success_url())


class ActivateView(TemplateView):
    template_name = 'account/activate.html'
    title = _('账号激活')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)

                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            user.is_active = True
            user.save()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return user

    def get_form_kwargs(self):
        kwargs = {}
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = {}
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('激活失败'),
                'validlink': False,
            })
        return context


class UpdateUserView(generic.UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'account/update.html'
    success_url = reverse_lazy('account:update_done')


class PasswordChangeView0(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    form_class = PasswordChangeForm0


class ResetPasswordView(PasswordResetConfirmView):
    form_class = ResetPasswordForm


def register_success(request):
    return render(request, 'account/register_success.html')


def update_success(request):
    return render(request, 'account/update_success.html')
