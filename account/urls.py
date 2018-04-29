from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path(r'', views.account_profile, name='profile'),
    path(r'register/', views.RegisterView.as_view(), name='register'),
    path(r'activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path(r'update/<int:pk>/', views.update_user, name='update_user'),
    path(r'register/done/', views.register_success, name='register_done'),
    path(r'password_change/', views.PasswordChangeView0.as_view(), name='password_change'),
    path(r'reset/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='password_reset_confirm'),
    # 头像
    path(r'avatar_change/', views.change, name='change_avatar'),
    # 用户列表/详情
    path(r'users/', views.UserListView.as_view(), name='user_list'),
    path(r'<str:username>/fans/', views.FansListView.as_view(), name='user_fans'),
    path(r'<str:username>/stars/', views.StarListView.as_view(), name='user_stars'),
    path(r'user/detail/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path(r'user/follow/', views.follow_user, name='follow_user'),
]
