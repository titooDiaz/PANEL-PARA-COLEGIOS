from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils.timezone import now
from .models import ChatMessage
from users.models import CustomUser
from asgiref.sync import sync_to_async
# load messages with scroll!
from django.core.paginator import Paginator
from channels.db import database_sync_to_async
from django.db.models import Q
import mimetypes

import redis
r = redis.Redis()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "typing":
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "typing_indicator",
                "user_id": data["sender_id"]
            })

        elif message_type == "delete":
            message_id = int(data["message_id"])
            await self.mark_message_deleted(message_id)

            await self.channel_layer.group_send(self.room_group_name, {
                "type": "deleted_message",
                "id": message_id
            })

        elif message_type == "stop_typing":
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "stop_typing_indicator",
                "user_id": data["sender_id"]
            })
        elif message_type == "highlight":
            message_id = int(data["message_id"])
            is_now_important = await self.mark_message_important(message_id)

            await self.channel_layer.group_send(self.room_group_name, {
                "type": "highlight_message",
                "id": message_id,
                "important": is_now_important  # ✅ Aquí sí lo tienes
            })
            
        elif message_type == "mark_all_seen":
            reader_id = data["user_id"]
            sender_id = data["receiver_id"]

            updated_ids = await self.mark_all_as_seen(reader_id, sender_id)

            last_seen_id = await self.get_last_seen_message_id(sender_id, reader_id)

            if last_seen_id:
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "seen_update",
                    "id": last_seen_id,
                    "user_id": reader_id
                })

        elif message_type == "seen":
            message_id = int(data["message_id"])
            user_id = int(data["user_id"])

            updated = await self.mark_message_read(message_id, user_id)

            if updated:
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "message_seen",
                    "id": message_id,
                    "seen_by": user_id
                })


        elif message_type == "chat":
            sender_id = int(data["sender_id"])
            receiver_id = int(data["receiver_id"])
            message = data["message"]
            file_data = data.get("file")
            reply_to_id = data.get("reply_to")

            msg = await self.save_message(sender_id, receiver_id, message, file_data, reply_to_id)

            # Enviamos mensaje con ID incluido
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "message": msg["message"],
                "sender_id": msg["sender_id"],
                "file": msg.get("file"),
                "id": msg["id"],
                "reply": msg.get("reply"),
                "important": msg.get("important", False)
            })
        elif message_type == "check_seen_status":
            sender_id = data["sender_id"]
            receiver_id = data["receiver_id"]

            last_seen_id = await self.get_last_seen_message_id(sender_id, receiver_id)

            if last_seen_id:
                await self.send(text_data=json.dumps({
                    "type": "seen",
                    "id": last_seen_id,
                    "user_id": receiver_id
                }))

        elif message_type == "mark_all_seen":
            user_id = data["user_id"]
            other_id = data["receiver_id"]
            updated_ids = await self.mark_all_as_seen(user_id, other_id)
            
            for msg_id in updated_ids:
                await self.send(text_data=json.dumps({
                    "type": "seen",
                    "id": msg_id
                }))

        elif message_type == "load_more":
            sender_id = int(data["sender_id"])
            receiver_id = int(data["receiver_id"])
            before_id = data.get("before_id")

            messages = await self.get_messages_before(sender_id, receiver_id, before_id)
            has_next = len(messages) == 25

            await self.send(text_data=json.dumps({
                "type": "more",
                "messages": messages,
                "has_next": has_next
            }))
    
    async def get_last_seen_message_id(self, sender_id, receiver_id):
        return await database_sync_to_async(lambda: (
            ChatMessage.objects
            .filter(sender_id=sender_id, receiver_id=receiver_id, read=True)
            .order_by('-sent_at')
            .values_list('id', flat=True)
            .first()
        ))()
    
    async def mark_message_read(self, message_id, user_id):
        try:
            message = await database_sync_to_async(ChatMessage.objects.select_related('receiver').get)(id=message_id)
            receiver_id = await database_sync_to_async(lambda: message.receiver.id)()

            if receiver_id == user_id:

                message.read = True
                await database_sync_to_async(message.save)()
                return True
            return False
        except ChatMessage.DoesNotExist:
            return False


    @database_sync_to_async
    def mark_all_as_seen(self, user_id, other_id):
        qs = ChatMessage.objects.filter(
            sender_id=other_id,
            receiver_id=user_id,
            read=False
        )
        updated_ids = list(qs.values_list('id', flat=True))
        qs.update(read=True, read_at=now())
        return updated_ids

    async def mark_message_read(self, message_id, user_id):
        try:
            message = await database_sync_to_async(ChatMessage.objects.select_related('receiver').get)(id=message_id)
            receiver_id = await database_sync_to_async(lambda: message.receiver.id)()

            if receiver_id == user_id:
                message.read = True
                message.read_at = now()
                await database_sync_to_async(message.save)()
                return True
            return False
        except ChatMessage.DoesNotExist:
            return False

    @database_sync_to_async
    def mark_message_important(self, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id)
            message.important = not message.important  # toggle
            message.save()
            return message.important
        except ChatMessage.DoesNotExist:
            return False  # o None si prefieres manejarlo distinto

    @database_sync_to_async
    def get_last_seen_message_id(self, viewer_id, chat_with_id):
        last_seen = ChatMessage.objects.filter(
            sender_id=viewer_id,
            receiver_id=chat_with_id,
            read=True
        ).order_by('-id').first()

        return last_seen.id if last_seen else None

    @database_sync_to_async
    def mark_message_deleted(self, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id)
            message.deleted = True
            message.save()
        except ChatMessage.DoesNotExist:
            pass


    @database_sync_to_async
    def get_messages_before(self, sender_id, receiver_id, before_id):
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)

        qs = ChatMessage.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).order_by("-id")


        if before_id:
            qs = qs.filter(id__lt=before_id)

        messages = list(qs[:25])

        return [{
            "message": m.content,
            "sender_id": m.sender.id,
            "important": m.important,
            "timestamp": m.sent_at.strftime("%H:%M"),
            "deleted": m.deleted,
            "id": m.id,
            "file": {
                "url": m.file.url,
                "type": mimetypes.guess_type(m.file.url)[0]
            } if m.file else None
        } for m in messages]

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message, file_data, reply_to_id=None):
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
        
        msg = ChatMessage(sender=sender, receiver=receiver, content=message)

        # 🔗 Save file if provided
        if file_data:
            relative_path = file_data['url'].replace('/media/', '')
            msg.file.name = relative_path

        # 🔁 Attach reply message if any
        reply_preview = None
        if reply_to_id:
            try:
                reply_obj = ChatMessage.objects.get(id=reply_to_id)
                msg.reply_to = reply_obj  # 🧠 Set FK relation
                reply_preview = reply_obj.content[:50] + "..."  # for front-end
            except ChatMessage.DoesNotExist:
                pass  # Silent fail if reply message not found

        msg.save()
        return {
            "id": msg.id,
            "message": msg.content,
            "sender_id": sender.id,
            "file": file_data,
            "important": msg.important,
            "reply": reply_preview  # this is optional, for displaying summary
        }

    async def seen_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "seen",
            "id": event["id"],
            "user_id": event["user_id"]
        }))

    async def highlight_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "highlight",
            "id": event["id"],
            "important": event["important"]
        }))

    async def message_seen(self, event):
        await self.send(text_data=json.dumps({
            "type": "seen",
            "id": event["id"],
            "seen_by": event["seen_by"]
        }))


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "file": event.get("file"),
            "id": event["id"],
            "reply": event.get("reply")
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user_id": event["user_id"]
        }))
    
    async def deleted_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "deleted",
            "id": event["id"]
        }))


    async def stop_typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "stop_typing",
            "user_id": event["user_id"]
        }))

import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer

r = redis.Redis()
watchers = {}  # {user_id: set of channel_names}


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.channel_name_id = self.channel_name

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

        # Marcar usuario como en línea
        r.set(f"user_online_{self.user.id}", "1", ex=60)
        print(f"[CONNECT] {self.user.id} está en línea")

        for channel in watchers.get(str(self.user.id), set()):
            await self.channel_layer.send(channel, {
                "type": "user_status_update",
                "user_id": self.user.id,
                "status": "online",
            })


    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "keep_alive":
            r.set(f"user_online_{self.user.id}", "1", ex=60)

        elif data["type"] == "watch":
            target_id = str(data["user_id"])
            watchers.setdefault(target_id, set()).add(self.channel_name)

            is_online = r.exists(f"user_online_{target_id}")
            await self.send(text_data=json.dumps({
                "type": "user_status",
                "user_id": int(target_id),
                "status": "online" if is_online else "offline"
            }))

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            r.delete(f"user_online_{self.user.id}")
            print(f"[DISCONNECT] {self.user.username} offline")

        for uid in list(watchers):
            watchers[uid].discard(self.channel_name)
            if not watchers[uid]:
                watchers.pop(uid)

        for channel in watchers.get(str(self.user.id), set()):
            await self.channel_layer.send(channel, {
                "type": "user_status_update",
                "user_id": self.user.id,
                "status": "offline"
            })

    async def user_status_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_status",
            "user_id": event["user_id"],
            "status": event["status"]
        }))
