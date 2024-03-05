import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from User.models import User
from .models import BasicGroup, PrivateChat
from .tasks import *


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_name = f"group_{self.group_id}_chat"
        self.transport = False
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        match data['type']:
            case 'chat':
                packet = data['data']
                group_id = packet['group_id']
                if self.transport:
                    group_id = self.group_id
                    packet['group_id'] = self.group_id
                async_backup_message.delay(packet)
                async_update_count.delay(group_id)
                print("***********\nget new chat packet:")
                print(packet)
                print("***********")
                await self.channel_layer.group_send(
                    self.room_name,
                    data,
                )
            case 'change':
                await self.change(data)

    async def chat(self, data):
        packet = data['data']
        if not self.transport or \
                (self.transport and int((self.channel_name.split('_'))[2]) == packet['group_id']):
            await self.send(json.dumps(packet))

    async def change(self, data):
        func = data['change']
        group_id = data['group_id']
        if self.group_id == 0:
            @database_sync_to_async
            def get_judge(data):
                judge = PrivateChat.objects.filter(member__user_id=data['user_id']).filter(
                    member__user_id=data['group_id'])
                flag = judge.exists()
                if flag:
                    res = judge[0]
                else:
                    res = None
                return res, flag

            judge, flag = await get_judge(data)
            if not flag:
                @database_sync_to_async
                def create_new_private_chat(data):
                    new_chat = PrivateChat.objects.create()
                    user_1 = User.objects.get(user_id=data['user_id'])
                    user_2 = User.objects.get(user_id=data['group_id'])
                    new_chat.member.add(user_1)
                    new_chat.member.add(user_2)
                    new_chat.save()
                    return new_chat.group_id

                self.group_id = await create_new_private_chat(data)
            else:
                self.group_id = judge.group_id
            self.transport = True
            self.channel_layer.group_discard(self.room_name, self.channel_name)
            self.channel_name = f"private_chat_{self.group_id}_{data['user_id']}"
            self.channel_layer.group_add(self.room_name, self.channel_name)
        if self.transport:
            data['group_id'] = self.group_id
            group_id = self.group_id

        @database_sync_to_async
        def async_check_team_room(group_id):
            name = f"group_{group_id}_chat_all_member"
            if conn.get(name) is None:
                group = BasicGroup.objects.get(group_id=group_id)
                user_set = set(group.get_member_id_list())
                conn.set(name, user_set, timeout=None)

        await async_check_team_room(group_id)
        match func:
            case 'enter':
                await self.handle_enter(data)
            case 'leave':
                await self.handle_leave(data)
            case _:
                await self.send("Invalid operation")

    async def handle_enter(self, data):
        print("**************\nhandle enter:")
        print(data)
        print("**************")
        user_id = data['user_id']
        group_id = data['group_id']
        print(f"> user {user_id} enter group {group_id}")
        room_name = f"group_{group_id}_chat_member"
        now = conn.get_or_set(room_name, default=set())
        now.add(user_id)
        conn.set(room_name, now, timeout=None)
        count_name = f"group_count_{group_id}_{user_id}"
        conn.set(count_name, 0, timeout=None)

    async def handle_leave(self, data):
        print("**************\nhandle leave:")
        print(data)
        print("**************")
        user_id = data['user_id']
        group_id = data['group_id']
        print(f"> user {user_id} leave group {group_id}")
        room_name = f"group_{group_id}_chat_member"
        now = conn.get_or_set(room_name, default=set())
        now.discard(user_id)
        conn.set(room_name, now, timeout=None)
        if self.transport:
            self.transport = False
            self.group_id = 0
