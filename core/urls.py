from django.contrib import admin
from django.urls import path, include
from .views import home

apps_urls = [
    path('api/auth/',include('apps.accounts.urls')),
    path('api/store/',include('apps.store.urls')),
    path('api/order/',include('apps.order.urls')),
    path('api/chat/',include('apps.chat.urls')),
]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path('',home,name='home')
    ]
    + apps_urls
)
