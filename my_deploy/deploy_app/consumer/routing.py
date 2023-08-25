from django.urls import path
from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from consumers import *

ws_router = URLRouter([
    path('ws/ssh/<int:id>', SshConsumer),
])
