from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from .consumers import GraphqlWsConsumer

# pylint: disable=C0103
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('graphql/', GraphqlWsConsumer),
    ])
})
