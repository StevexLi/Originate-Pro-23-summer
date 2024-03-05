from channels.routing import URLRouter
from django.urls import path
from Chat.routing import websocket_urlpatterns as chat_route
from Notification.routing import websocket_urlpatterns as noti_route
websocket_urlpatterns = [
    path('ws/chat/', URLRouter(chat_route)),
    path('ws/notification/', URLRouter(noti_route)),
]