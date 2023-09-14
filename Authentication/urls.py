from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.UserLoginView, name='login'),
    path('logout', views.UserLogoutView, name='logout'),
    path('register', views.UserRegisterView, name='register'),

    # |------------------------SOCIAL AUTH--------------------------|
    path('social-auth', include('social_django.urls', namespace='social')),

    # |------------------------FORGOT PASSWORD--------------------------|
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # |------------------------CHANGE PASSWORD--------------------------|
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]