from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from account.forms import (PasswordChangeForm0, RegisterForm, ResetPasswordForm, UpdateUserForm)


@login_required
def account_profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


class RegisterView(generic.CreateView):
    # todo add email verification
    # todo add auto login
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:register_done')


class UpdateUserView(generic.UpdateView):
    model = get_user_model()
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
