from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage
from users.models import CustomUser  # Ajusta según tu modelo
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "file": event.get("file")  # <--- asegurarse de que esté
        }))


    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Datos recibidos:", data)
        message = data["message"]
        sender_id = data["sender_id"]
        receiver_id = data["receiver_id"]
        file_data = data.get("file")  # {'url': ..., 'name': ...}

        await self.save_message(sender_id, receiver_id, message, file_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
                "file": file_data
            }
        )

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message, file_data):
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
        msg = ChatMessage(sender=sender, receiver=receiver, content=message)

        if file_data:
            # Quitar '/media/' para que coincida con el path relativo que espera FileField
            relative_path = file_data['url'].replace('/media/', '')
            msg.file.name = relative_path  # ← guardamos la referencia directamente

        msg.save()
