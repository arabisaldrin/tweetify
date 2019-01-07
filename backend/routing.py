from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

from backend.api import tweet

websocket_urlpatterns = [
    path('ws/tweet_stream/user/<int:user_id>', tweet.IOTweetConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
