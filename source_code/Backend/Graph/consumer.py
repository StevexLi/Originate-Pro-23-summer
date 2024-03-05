from channels.generic.websocket import AsyncWebsocketConsumer
import json
class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        graph_id = self.scope['url_route']['kwargs']['graph_id']
        self.room_name = f"graph_{graph_id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        graph_content = data.get('content', '')
        user_id = data.get('user_id')
        project_id = data.get('project_id')
        name = data.get('name')
        graph_id = data.get('graph_id')
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send.graph_content',
                'content': graph_content,
                'user_id': user_id,
                'project_id': project_id,
                'name': name,
                'graph_id': graph_id,
            }
        )
    async def send_graph_content(self, event):
        graph_content = event.get('content')
        user_id = event.get('user_id')
        project_id = event.get('project_id')
        name = event.get('name')
        graph_id = event.get('graph_id')
        await self.send(json.dumps({
            'content': graph_content,
            'user_id': user_id,
            'project_id': project_id,
            'name': name,
            'graph_id': graph_id,
        }))
