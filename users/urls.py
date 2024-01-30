from django.urls import path, re_path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^register/$', register, name='register'),
    re_path(r'^login/$', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="users/password_reset.html"),
         name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="users/appointment_confirm_delete.html"),
         name='password_reset_confirm'),
]
