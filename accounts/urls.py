from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserAuthenticationForm


urlpatterns = [
    path('', views.user_profile, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts\login.html',authentication_form=UserAuthenticationForm), name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('passwordrecovery/', views.forgot_password, name='forgot_password'),
    path('register/', views.user_register, name='register'),
    path('varify/<slug:token>', views.varify_token, name='varify'),
    path('profile/image/update/',views.profile_image_update,name="image_update"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]
