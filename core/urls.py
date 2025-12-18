from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static

apps_urls = [
    path('api/auth/',include('apps.accounts.urls')),
    path('api/store/',include('apps.store.urls')),
    path('api/order/',include('apps.order.urls')),
    path('api/chat/',include('apps.chat.urls')),
    path('api/transaction/',include('apps.transaction.urls')),

]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path('',home,name='home')
    ]
    + apps_urls
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)