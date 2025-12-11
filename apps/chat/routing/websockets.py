from django.urls import path, include
from apps.chat.consumers.communicates import CommunicationConsumer 

websocket_urlpatterns = (
    [ 
        path("ws/chat/channel/<uuid:channel_id>/connect/", CommunicationConsumer.as_asgi())

    ]
)