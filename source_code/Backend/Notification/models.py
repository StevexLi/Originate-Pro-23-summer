from django.db import models
from abc import abstractmethod
from Chat.models import BasicGroup
from Team.models import Team
from User.models import User


# Create your models here.
class BasicNotification(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receiver')
    processed = models.BooleanField(default=False)
    type = models.CharField(default='normal', max_length=30)

    @abstractmethod
    def get_notification_dict(self):
        pass


class TeamNotification(BasicNotification):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)

    def get_notification_dict(self):
        res = {
            'id': self.id,
            'content': self.content,
            'group_type': "team",
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'processed': self.processed,
            'team_id': self.team.id,
            'type': self.type,
        }
        return res


class GroupNotification(BasicNotification):
    group = models.ForeignKey(to=BasicGroup, on_delete=models.CASCADE)

    def get_notification_dict(self):
        res = {
            'id': self.id,
            'content': self.content,
            'group_type': "group",
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'processed': self.processed,
            'group_id': self.group.group_id,
            'type': self.type,
        }
        return res
