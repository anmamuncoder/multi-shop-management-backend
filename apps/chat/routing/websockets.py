from django.urls import path, include
from apps.chat.consumers.communicates import CommunicationConsumer 
websocket_urlpatterns = (
    [
        path("ws/shop/<slug:shop_slug>/order/<uuid:order_id>/", CommunicationConsumer.as_asgi())


    ]
)