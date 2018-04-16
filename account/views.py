from avatar.forms import PrimaryAvatarForm, UploadAvatarForm
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.utils import invalidate_cache
from avatar.views import _get_avatars, _get_next
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView, \
    PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ugettext as temp
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from account.forms import (PasswordChangeForm0,
                           RegisterForm,
                           ResetPasswordForm,
                           UpdateProfileForm,
                           UpdateUserForm)
from account.models import Contact, Profile
from blog.models import Article

User = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'activate_account'
INTERNAL_RESET_SESSION_TOKEN = '_activate_account_token'


@login_required
def account_profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


class RegisterView(generic.CreateView):
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
        profile = Profile.objects.create(user=user)
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
        messages.success(self.request, '激活成功')
        return redirect('account:profile')

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            user.is_active = True
            user.save()
            login(self.request, user)
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


@login_required
def update_user(request, pk):
    """更新用户信息"""
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        user_form = UpdateUserForm(instance=user, data=request.POST)
        profile_form = UpdateProfileForm(instance=user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "更新成功")

    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)
    return render(request, 'account/update.html',
                  {"user_form": user_form,
                   "profile_form": profile_form})


class PasswordChangeView0(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('account:profile')
    success_message = '修改密码成功'
    form_class = PasswordChangeForm0


class ResetPasswordView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = ResetPasswordForm
    success_message = '密码重置完成'
    success_url = reverse_lazy('account:profile')


def register_success(request):
    return render(request, 'account/register_success.html')


@login_required
def change(request, extra_context=None, next_override=None,
           upload_form=UploadAvatarForm, primary_form=PrimaryAvatarForm,
           *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial': {'choice': avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
                                       user=request.user,
                                       avatars=avatars, **kwargs)
    if request.method == "POST":
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(
                    id=primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            invalidate_cache(request.user)
            messages.success(request, temp("成功更新头像"))
        if updated:
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return redirect(next_override or _get_next(request))

    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'primary_avatar_form': primary_avatar_form,
        'next': next_override or _get_next(request)
    }
    context.update(extra_context)
    return render(request, 'account/avatar/change.html', context)


class UserListView(generic.ListView):
    """展示全部用户列表"""
    queryset = User.objects.filter(is_active=True)
    context_object_name = 'users'
    template_name = 'account/user/list.html'


class FansListView(UserListView):
    """展示粉丝列表"""

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        fans = user.fan0.all()
        return fans


class StarListView(UserListView):
    """展示关注的人列表"""

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        stars = user.star0.all()
        return stars


class UserDetailView(generic.DetailView):
    """展示用户详情"""
    model = User
    context_object_name = 'user'
    template_name = 'account/user/detail.html'

    def get_object(self, queryset=None):
        """通过用户名获取用户"""
        username = self.kwargs['username']
        obj = get_object_or_404(User, username=username)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        articles = Article.published.filter(author=user).order_by('-created')
        context['articles'] = articles
        return context


@login_required
def follow_user(request):
    """（取消）关注用户"""
    user_id = int(request.POST.get('user_id'))
    action = str(request.POST.get('action'))
    if user_id == request.user.id:
        return JsonResponse({'action': 'self'})
    if user_id and action:
        try:
            if action == '关注':
                Contact.objects.create(fans=request.user,
                                       star_id=user_id)
                json = {'action': '取消关注'}
            else:
                Contact.objects.filter(fans=request.user,
                                       star_id=user_id).delete()
                json = {'action': '关注'}
            return JsonResponse(json)
        except User.DoesNotExist:
            return JsonResponse({})
    return JsonResponse({})
