# Library
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# Internal
from .views import RegisterView, CustomTokenObtainPairView

app_name = "accounts"
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomTokenObtainPairView.as_view(),name="login"),
    path('login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),
]

