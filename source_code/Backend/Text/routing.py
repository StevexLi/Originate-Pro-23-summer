from django.urls import path
from .consumer import TextConsumer

websocket_urlpatterns = [
    path('<int:text_id>', TextConsumer.as_asgi()),
]
