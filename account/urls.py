from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path(r'profile/', views.account_profile, name='profile'),
    path(r'register/', views.RegisterView.as_view(), name='register'),
    path(r'update/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path(r'register/done/', views.register_success, name='register_done'),
    path(r'update/done/', views.update_success, name='update_done'),
    path(r'password_change/', views.PasswordChangeView0.as_view(), name='password_change'),
    path(r'reset/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='password_reset_confirm'),
]
