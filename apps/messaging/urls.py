from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateMessageView, MessageCampaignView, MessageLogView,CustomerView

routers = DefaultRouter()
routers.register('templates', TemplateMessageView, basename='templates')
routers.register('campaigns', MessageCampaignView, basename='campaigns')
routers.register('logs', MessageLogView, basename='logs')

routers.register('customers', CustomerView, basename='customers')

urls_owner = [ 
]

urls_customer = [ 
]

app_name = "messaging"
urlpatterns = (
    []
    + urls_owner
    + urls_customer
    + routers.urls
)
