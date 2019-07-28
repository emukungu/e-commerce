import asyncio
import json 
from channels.consumer import AsyncConsumer   
from channels.db import database_sync_to_async
from authenticate.models import User

from .models import Orders

class OrderConsumer(AsyncConsumer):
  async def websocket_connect(self, event):
    print('connected', event)
    await self.send({
      'type': 'websocket.accept'
    })
    loggedin_user = self.scope['user']
    order_status = await self.get_orders(loggedin_user)
    await self.send({
      'type': 'websocket.send',
      'text': order_status
    })

  async def websocket_receive(self, event):
    print("receive", event)

  async def websocket_disconnect(self, event):
    print("disconnected", event)
  
  @database_sync_to_async
  def get_orders(self, user):
    return Orders.objects.filter(ordered_by = self.user.id) #check user id
    