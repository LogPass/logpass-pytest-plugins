import os

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        path('test/<anything>', AsyncJsonWebsocketConsumer.as_asgi()),
    ]),
})
