import json
from itertools import chain

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from Chat.models import TeamGroupChat, GroupChat
from Utlis.RedisUtlis import conn
from Team.models import Team
from User.models import User
from .models import TeamNotification, GroupNotification
from .tasks import *
from Text.models import Text
from distutils.util import strtobool


class AsyncNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notification', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('notification', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        match data['type']:
            case 'notification':
                await self.notification(data)
            case 'invite.response':
                await self.invite_response(data)
            case 'at_jump':
                await self.at_jump(data)
            case 'func':
                await self.func(data)

    async def func(self, data):
        func = data['func']
        match func:
            case "process":
                await self.process_notification(data)
            case "delete":
                await self.delete_notification(data)
            case "get":
                await self.get_notification(data)
            case _:
                await self.send('Invalid operation')

    async def notification(self, data):
        print('get data: ' + str(data))
        noti_type = data['noti_type']
        match noti_type:
            case 'invite':
                data['data']['type'] = 'invite'
            case 'at_document':
                data['data']['type'] = 'at_document'
            case 'at_chat':
                data['data']['type'] = 'at_chat'
            case _:
                data['data']['type'] = 'normal'
        await self.channel_layer.group_send(
            'notification',
            {
                "type": "client.send",
                "data": json.dumps(data['data']),
            }
        )

    async def at_jump(self, data):
        type_info = data['at_type']
        match type_info:
            case 'document':
                @database_sync_to_async
                def create_message_team(data):
                    sender_id = data['sender_id']
                    sender = User.objects.get(user_id=sender_id)
                    document_id = data['document_id']
                    document = Text.objects.get(id=document_id)
                    content = f"{sender.username}邀请您参与文档{document.name}的编辑"
                    entry = TeamNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                                            sender_id=sender_id,
                                                            team_id=data['team_id'],
                                                            type='at_jump')
                    res_dict = entry.get_notification_dict()
                    res_dict['project_id'] = data['project_id']
                    res_dict['document_id'] = data['document_id']
                    entry_dict = {
                        'type': 'notification',
                        'noti_type': 'at_document',
                        'data': res_dict,
                    }
                    return entry_dict

                res_dict = await create_message_team(data)
                await self.channel_layer.group_send(
                    'notification',
                    res_dict,
                )
            case 'chat':
                @database_sync_to_async
                def create_message_group(data):
                    sender_id = data['sender_id']
                    sender = User.objects.get(user_id=sender_id)
                    group_id = data['group_id']
                    group = \
                        (list(TeamGroupChat.objects.filter(group_id=group_id)) + list(GroupChat.objects.filter(group_id=group_id)))[
                            0]
                    content = f"{sender.username}在{group.get_name()}中at了你，快去看看吧"
                    entry = GroupNotification.objects.create(content=content, receiver_id=data['user_id'],
                                                             sender_id=sender_id,
                                                             group_id=group.group_id,
                                                             type='at_jump')
                    res_dict = entry.get_notification_dict()
                    entry_dict = {
                        'type': 'notification',
                        'noti_type': 'at_chat',
                        'data': res_dict,
                    }
                    return entry_dict
                res_dict = await create_message_group(data)
                await self.channel_layer.group_send(
                    'notification',
                    res_dict,
                )
            case _:
                res = {'error': 'Invalid at type'}
                await self.send(json.dumps(res))

    async def invite_response(self, data):
        print('get data: ' + str(data))
        state = strtobool(data['response'])
        invite_type = data['group_type']

        @database_sync_to_async
        def create_message_add_member_team(data):
            sender = User.objects.get(user_id=data['sender_id'])
            sender_name = sender.username
            team = Team.objects.get(id=data['team_id'])
            team_name = team.name
            if sender.user_id in team.get_all_id_list():
                res_dict = {
                    'error': '你已经加入此团队',
                }
                flag = False
                return res_dict, flag
            content = f"{sender_name}同意加入{team_name}团队"
            entry = TeamNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                                    sender_id=sender.user_id,
                                                    team_id=team.id,
                                                    type='normal')
            team.member.add(sender)
            team.save()
            team_group_chat = TeamGroupChat.objects.get(team=team)
            team_group_chat.member.add(sender)
            entry_dict = {
                'type': 'notification',
                'noti_type': 'normal',
                'data': entry.get_notification_dict(),
            }
            conn.delete(f"group_{team_group_chat.group_id}_chat_all_member")
            flag = True
            return entry_dict, flag

        @database_sync_to_async
        def create_message_team(data):
            sender = User.objects.get(user_id=data['sender_id'])
            sender_name = sender.username
            team = Team.objects.get(id=data['team_id'])
            team_name = team.name
            if sender.user_id in team.get_all_id_list():
                res_dict = {
                    'error': '你已经加入此团队',
                }
                flag = False
                return res_dict, flag
            content = f"很遗憾，{sender_name}拒绝了加入{team_name}团队的邀请"
            entry = TeamNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                                    sender_id=sender.user_id,
                                                    team_id=team.id, type='normal')
            entry_dict = {
                'type': 'notification',
                'noti_type': 'normal',
                'data': entry.get_notification_dict(),
            }
            flag = True
            return entry_dict, flag

        @database_sync_to_async
        def create_message_add_member_group(data):
            sender = User.objects.get(user_id=data['sender_id'])
            sender_name = sender.username
            group = GroupChat.objects.get(group_id=data['group_id'])
            group_name = group.name
            if sender.user_id in group.get_member_id_list():
                res_dict = {
                    'error': '你已经加入此团队',
                }
                flag = False
                return res_dict, flag
            content = f"{sender_name}同意加入{group_name}群组"
            entry = GroupNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                                    sender_id=sender.user_id,
                                                    group_id=group.group_id,
                                                    type='normal')
            group.member.add(sender)
            group.save()
            entry_dict = {
                'type': 'notification',
                'noti_type': 'normal',
                'data': entry.get_notification_dict(),
            }
            conn.delete(f"group_{group.group_id}_chat_all_member")
            flag = True
            return entry_dict, flag

        @database_sync_to_async
        def create_message_group(data):
            sender = User.objects.get(user_id=data['sender_id'])
            sender_name = sender.username
            group = GroupChat.objects.get(group_id=data['group_id'])
            group_name = group.name
            if sender.user_id in group.get_member_id_list():
                res_dict = {
                    'error': '你已经加入此团队',
                }
                flag = False
                return res_dict, flag
            content = f"很遗憾，{sender_name}拒绝了加入{group_name}团队的邀请"
            entry = GroupNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                                    sender_id=sender.user_id,
                                                    group_id=group.group_id, type='normal')
            entry_dict = {
                'type': 'notification',
                'noti_type': 'normal',
                'data': entry.get_notification_dict(),
            }
            flag = True
            return entry_dict, flag

        if invite_type == 'team':
            if state:
                res_dict, flag = await create_message_add_member_team(data)
            else:
                res_dict, flag = await create_message_team(data)
        else:
            if state:
                res_dict, flag = await create_message_add_member_group(data)
            else:
                res_dict, flag = await create_message_group(data)
        if not flag:
            await self.send(json.dumps(res_dict))
        else:
            await self.channel_layer.group_send(
                'notification',
                res_dict,
            )

    async def client_send(self, data):
        await self.send(data['data'])

    async def process_notification(self, data):
        data = data['data']
        async_process_notification.delay(data)

    async def delete_notification(self, data):
        data = data['data']
        async_delete_notification.delay(data)

    async def get_notification(self, data):
        data = data['data']
        user_id = data[0]

        @database_sync_to_async
        def async_get_message(user_id):
            try:
                message_set = (list(TeamNotification.objects.filter(receiver_id=user_id)) +
                               list(GroupNotification.objects.filter(receiver_id=user_id)))
                res = []
                for _ in message_set:
                    res.append(_.get_notification_dict())
                res = sorted(res, key=lambda x: (x['processed'], -x['id']))
            except Exception as e:
                print(e)
                res = "get notification failed"
            return res

        res = await async_get_message(user_id)
        res = {"data": {
            'data': res,
        }
        }
        await self.send(json.dumps(res))
