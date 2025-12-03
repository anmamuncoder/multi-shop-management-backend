# Library
from django.urls import path, include
# Internal
from .views import RegisterView

app_name = "accounts"
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register')
]

