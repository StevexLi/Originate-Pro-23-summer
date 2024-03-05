from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TextConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        text_id = self.scope['url_route']['kwargs']['text_id']
        self.room_name = f"text_{text_id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get('content')
        user_id = data.get('user_id')
        project_id = data.get('project_id')
        name = data.get('name')
        text_id = data.get('text_id')
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send.text_content',
                'content': content,
                'user_id': user_id,
                'project_id': project_id,
                'name': name,
                'text_id': text_id,
            }
        )





    async def send_text_content(self, event):
        content = event.get('content')
        user_id = event.get('user_id')
        project_id = event.get('project_id')
        name = event.get('name')
        text_id = event.get('text_id')



        await self.send(json.dumps({
            'content': content,
            'user_id': user_id,
            'project_id': project_id,
            'name': name,
            'text_id': text_id,
        }))
