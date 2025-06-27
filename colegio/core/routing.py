# core/routing.py
from django.urls import re_path, path
from information.consumers import ChatConsumer, PresenceConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/online/$', PresenceConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<teacher_id>\d+)/$', ChatConsumer.as_asgi()),
]
