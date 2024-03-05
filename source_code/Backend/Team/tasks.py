from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Notification.models import TeamNotification
from User.models import User
from Team.models import Team
from Backend_Su23.celery import app
from Chat.models import TeamGroupChat


@app.task
def async_delete_member(data):
    sender = User.objects.get(user_id=data['sender_id'])
    sender_name = sender.username
    team = Team.objects.get(id=data['team_id'])
    team_name = team.name
    content = f"{sender_name}已经将您踢出{team_name}团队"
    entry = TeamNotification.objects.create(content=content, receiver_id=data['receiver_id'],
                                            sender_id=sender.user_id,
                                            team_id=team.id,
                                            type='normal')
    entry_dict = {
        'type': 'notification',
        'noti_type': 'normal',
        'data': entry.get_notification_dict(),
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('notification', entry_dict)


@app.task
def async_delete_member_from_team_group(team_id, user_id):
    group = TeamGroupChat.objects.get(team_id=team_id)
    user = User.objects.get(user_id=user_id)
    group.member.remove(user)
    group.save()
