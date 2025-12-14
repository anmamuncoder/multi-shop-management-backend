from django.urls import path , include
from .views import ChannelView, MessageView

urlpatterns = (
    [
        path('channel/', ChannelView.as_view(), name='user-chats'),
        path("<uuid:channel_id>/messages/", MessageView.as_view(), name="messages"),

    ] 
)
