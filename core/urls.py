from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

apps_urls = [
    path('api/auth/',include('apps.accounts.urls')),
    path('api/store/',include('apps.store.urls')),
    path('api/order/',include('apps.order.urls')),
    path('api/chat/',include('apps.chat.urls')),
    path('api/transaction/',include('apps.transaction.urls')),
    path('',include('apps.cms.urls')),

]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
         
    ]
    + apps_urls
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)