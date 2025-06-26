from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage
from users.models import CustomUser
from asgiref.sync import sync_to_async

import redis
r = redis.Redis()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")  # default is chat
        # Handle typing indicator
        if message_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_indicator",
                    "user_id": data["sender_id"]
                }
            )

        elif message_type == "stop_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "stop_typing_indicator",
                    "user_id": data["sender_id"]
                }
            )

        elif message_type == "chat":
            message = data["message"]
            sender_id = data["sender_id"]
            receiver_id = data["receiver_id"]
            file_data = data.get("file")  # Optional file data

            # Save message to DB
            await self.save_message(sender_id, receiver_id, message, file_data)

            # Broadcast message to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": sender_id,
                    "file": file_data
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "file": event.get("file")
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user_id": event["user_id"]
        }))

    async def stop_typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "stop_typing",
            "user_id": event["user_id"]
        }))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message, file_data):
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
        msg = ChatMessage(sender=sender, receiver=receiver, content=message)

        if file_data:
            relative_path = file_data['url'].replace('/media/', '')
            msg.file.name = relative_path

        msg.save()
        
import json
import asyncio
import redis
from channels.generic.websocket import AsyncWebsocketConsumer

r = redis.Redis()
watchers = {}  # {user_id: set of channel_names watching this user}

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.channel_id = self.channel_name

        if not self.user.is_authenticated:
            await self.close()
            return

        self.user_id = str(self.user.id)
        await self.accept()

        # 🔼 Increment active connection count for this user
        r.incr(f"user_connections_{self.user_id}")
        r.set(f"user_online_{self.user_id}", "1", ex=60)

        # 🟢 If this is the first connection, notify watchers
        if r.get(f"user_connections_{self.user_id}") == b'1':
            for watcher in watchers.get(self.user_id, set()):
                await self.channel_layer.send(watcher, {
                    "type": "user_status_update",
                    "user_id": int(self.user_id),
                    "status": "online",
                })

    async def disconnect(self, close_code):
        # ⏳ Wait briefly to avoid false offline on page transitions
        await asyncio.sleep(1)

        remaining = r.decr(f"user_connections_{self.user_id}")

        if remaining <= 0:
            # 🔴 No more active connections: user is offline
            r.delete(f"user_online_{self.user_id}")
            r.delete(f"user_connections_{self.user_id}")

            for watcher in watchers.get(self.user_id, set()):
                await self.channel_layer.send(watcher, {
                    "type": "user_status_update",
                    "user_id": int(self.user_id),
                    "status": "offline",
                })

        # 🧹 Clean up: remove this channel from all watch lists
        for uid in list(watchers):
            watchers[uid].discard(self.channel_id)
            if not watchers[uid]:
                watchers.pop(uid)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "keep_alive":
            # 🔁 Refresh TTL to keep user marked online
            r.set(f"user_online_{self.user_id}", "1", ex=60)

        elif data["type"] == "watch":
            # 👁️ This client wants to watch another user's status
            target_id = str(data["user_id"])
            watchers.setdefault(target_id, set()).add(self.channel_id)

            is_online = r.exists(f"user_online_{target_id}")
            await self.send(text_data=json.dumps({
                "type": "user_status",
                "user_id": int(target_id),
                "status": "online" if is_online else "offline"
            }))

    async def user_status_update(self, event):
        # 🔔 Broadcast status change to a watcher
        await self.send(text_data=json.dumps({
            "type": "user_status",
            "user_id": event["user_id"],
            "status": event["status"],
        }))
