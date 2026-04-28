from django.urls import path
from .views import *

urlpatterns = [
    # AUTH
    path("register/" , RegisterView.as_view()),
    path("login/" , LoginView.as_view()),
    path("verify-otp/" , VerifyOtpView.as_view()),
    
    # Forgot password
    path("forgot-password/" , ForgotPasswordView.as_view()),
    path('verify-password/' , VerifyPasswordView.as_view()),
    
    # Profile
    path("profile-list/" , ProfileView.as_view()),
    path("profile-update/" , ProfileUpdateView .as_view())
    
]