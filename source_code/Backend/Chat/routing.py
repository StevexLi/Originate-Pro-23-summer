from django.urls import path

from .consumer import *

websocket_urlpatterns = [
    path('group/<int:group_id>/', GroupChatConsumer.as_asgi()),
]

