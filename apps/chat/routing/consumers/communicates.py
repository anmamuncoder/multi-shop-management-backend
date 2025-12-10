from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CustomerVsShopOwner(AsyncWebsocketConsumer):
    async def connect(self):
        await self.send(json.dumps({"message":"Hello"}))
        return await super().connect()
    
    async def disconnect(self, code):
        return await super().disconnect(code)
    