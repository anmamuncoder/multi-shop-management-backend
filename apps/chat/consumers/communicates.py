from channels.generic.websocket import AsyncWebsocketConsumer
import json
from apps.chat.models import Channel, Message
from apps.accounts.models import User
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
  
class CommunicationConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # ----------------------
        # Extract token from query string
        # ----------------------
        query_string = self.scope['query_string'].decode()
        token = None
        for part in query_string.split("&"):
            if part.startswith("token="):
                token = part.split("=")[1]
        
        if not token:
            await self.close()
            return
        
        # ----------------------
        # Authenticate user
        # ----------------------
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            self.user = await database_sync_to_async(User.objects.get)(id=user_id)
        except Exception:
            await self.close()
            return 

        # --------------------------------
        # Get URL Params & channel object
        # --------------------------------- 
        self.channel_id = self.scope["url_route"]["kwargs"]['channel_id']  
        # Get channel object
        self.channel_obj = await self.get_channel_object()
        if not self.channel_obj:
            await self.close()
            return 
        
        # --------------------------------
        # Channel Group Create & Accepted
        # ---------------------------------
        # Group name
        self.group_name = f"channel_{self.channel_obj.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send(json.dumps({"status": "connected", "message":{"sender": self.user.email,"user_role": self.user.role }}))


    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
 
    async def receive(self, text_data=None, bytes_data=None):
        """
        Handle incoming message from WebSocket 
        When user sends message; save + broadcast ,[client -> server] 
        """

        if text_data:
            data = json.loads(text_data)
            message_text = data.get("message")

            # Save message to database
            message_obj = await self.create_message(message_text)

            # Broadcast to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_message", # < -- mandatory!
                    "status": "ongoing",
                    "message": {
                        "id": str(message_obj.id),
                        "sender": self.user.email,
                        "sender_role": self.user.role,
                        "message": message_obj.message,
                        "created_at": str(message_obj.created_at)
                    }
                }
            ) 

    async def send_message(self, event):
        """
        Receive message from group \
        When server broadcasts to clients , [server -> client]
        """
        await self.send(text_data=json.dumps({
            "status": event.get("status"),  # include status
            "message": event.get("message")
        }))

    # -------------------------------------
    # Using Database to save and query
    # -------------------------------------
    @database_sync_to_async
    def get_channel_object(self):
        try:
            if self.user.role == "customer":
                return Channel.objects.get(id=self.channel_id,customer=self.user,is_active=True)
            if self.user.role == "shop_owner":
                return Channel.objects.get(id=self.channel_id,shop__owner=self.user,is_active=True)
        except ObjectDoesNotExist:
            return None
        
    @database_sync_to_async
    def create_message(self, message_text):
        return Message.objects.create(channel=self.channel_obj,sender=self.user,message=message_text)
