from . import views

from django.urls import path



app_name = 'CustomUser'

urlpatterns = [
    path('create/', views.UserCreate.as_view(), name='create'),
    path('login/', views.UserLogin.as_view(), name= 'login'),
    path('profile/<uuid:uuid_value>/', views.UserProfile.as_view(), name = 'profile'),
    path('update/<uuid:uuid_value>/', views.UserUpdate.as_view(), name = 'update'),
    path('change_email/', views.UserOTPVerifyEmailChange.as_view(), name = 'change_email'),
    path('password_change/', views.UserPasswordChange.as_view(), name = 'password_change'),
    path('password_reset/', views.UserPasswordReset.as_view(), name = 'password_reset'),
    path('password_reset_done/', views.UserPasswordResetDone.as_view(), name = 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirm.as_view(), name = 'password_reset_confirm'),
    path('logout/', views.UserLogout.as_view(), name = 'logout'),
    path('delete/', views.UserDelete.as_view(), name = 'delete'),
    path('otp_verify/', views.UserOTPVerify.as_view(), name= 'otp_verify'),
    ]


