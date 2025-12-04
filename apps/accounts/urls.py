# Library
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# Internal
from .views import RegisterView, CustomTokenObtainPairView,UserView,SendOTPView,VerifyOTPView

app_name = "accounts"
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomTokenObtainPairView.as_view(),name="login"),
    path('login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),

    path('profile/',UserView.as_view(),name="profile"),

    path('email/resend/otp/',SendOTPView.as_view(),name="email_resend_otp"),
    path('email/verify/otp/',VerifyOTPView.as_view(),name="email_verify_otp"),
]

