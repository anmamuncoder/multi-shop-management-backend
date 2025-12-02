from django.contrib import admin
from django.urls import path, include

apps_urls = [

]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
    ]
    + apps_urls
)
