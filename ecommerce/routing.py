from django.config.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from cahannels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, AllowedHostsOriginValidator

from orders.consumers import OrderConsumer
application = ProtocolTypeRouter({
  'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
      URLRouter(
        [
          url(r'^<slug>/', OrderConsumer )
        ]
      )
    )
  )
})