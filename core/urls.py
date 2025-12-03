from django.contrib import admin
from django.urls import path, include

apps_urls = [
    path('api/auth/',include('apps.accounts.urls'))
]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
    ]
    + apps_urls
)
