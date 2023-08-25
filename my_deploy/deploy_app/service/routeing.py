from django.urls import path
from ..consumer import routing
from channels.routing import ProtocolTypeRouter


application = ProtocolTypeRouter({
    'websocket': routing.ws_router
})
