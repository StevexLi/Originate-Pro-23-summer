from django.urls import path
from .consumer import AsyncNotificationConsumer
websocket_urlpatterns = [
    path('', AsyncNotificationConsumer.as_asgi()),
]