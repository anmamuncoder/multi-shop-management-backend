from django.urls import path , include
from .views import ChannelView, MessageView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('channels',ChannelView,basename='channels')

app_name = 'chat'
urlpatterns = (
    [
        # path('channel/', ChannelView.as_view(), name='user-chats'),
        path("<uuid:channel_id>/messages/", MessageView.as_view(), name="messages"),

    ] + router.urls
)
