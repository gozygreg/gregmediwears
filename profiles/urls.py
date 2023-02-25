from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    # path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    # path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    # path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    # path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

    # Login/ logout urls
    path('my-login', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name='user-logout'),

    # Dashbooard / profile urls
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile-management', views.profile_management, name='profile-management'),
    path('profile-delete', views.profile_delete, name='profile-delete'),

    # # Password management to submit email form
    # path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),

    # # Password management to let user know that a password reset email has been sent
    # path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # # Password rest link
    # path('reset/<uidb64>/token/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # # Password success message
    # path('reset_password_complate', auth_views.PasswordResetCompleteView(), name='password_reset_complete')

]