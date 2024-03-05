from django.urls import path
from .consumer import GraphConsumer

websocket_urlpatterns = [
    path('<int:graph_id>', GraphConsumer.as_asgi()),
]
