import time
from abc import abstractmethod
from django.db import models
from Team.models import Team
from User.models import User
from Utlis.BucketUtlis import bucket
from properties import BUCKET_ROOT


# Create your models here.
class BasicGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    member = models.ManyToManyField(to=User)

    def get_member_id_list(self):
        res = []
        for _ in self.member.all():
            res.append(_.user_id)
        return res

    def get_member_info_list(self):
        res = []
        for _ in self.member.all():
            res.append(_.get_user_info_detail())
        return res

    @abstractmethod
    def get_name(self, user_id=None):
        pass

    @abstractmethod
    def get_group_info(self, user_id=None):
        pass

    def get_history(self):
        res = MessageEntry.objects.filter(group_id=self.group_id).order_by("raw_timestamp")
        return res


class TeamGroupChat(BasicGroup):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='Team')

    def get_name(self, user_id=None):
        return self.team.name + '团队群聊'

    def get_group_info(self, user_id=None):
        res = {
            "group_id": self.group_id,
            "type": self.type,
            "name": self.get_name(),
            "member": self.get_member_id_list(),
            "icon_address": self.team.get_icon(),
            "member_info": self.get_member_info_list(),
        }
        return res


class GroupChat(BasicGroup):
    name = models.CharField(max_length=40)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='Group')
    has_icon = models.BooleanField(default=False)

    def get_group_info(self, user_id=None):
        res = {
            "group_id": self.group_id,
            "type": self.type,
            "name": self.get_name(),
            "member": self.get_member_id_list(),
            "icon_address": self.get_icon(),
            "member_info": self.get_member_info_list(),
        }
        return res

    def get_name(self, user_id=None):
        return self.name

    def get_icon(self):
        if self.has_icon:
            prefix = 'icon/group/' + str(self.id)
            name = bucket.list_file(prefix)
            res = BUCKET_ROOT + '/' + name
        else:
            res = BUCKET_ROOT + '/icon/group/default_icon.jpg'
        return 'https://' + res


class PrivateChat(BasicGroup):
    type = models.CharField(max_length=10, default='Private')

    def get_name(self, user_id=None):
        pass

    def get_group_info(self, user_id=None):
        member_list = self.get_member_id_list()
        if user_id == member_list[0]:
            search_id = member_list[1]
        else:
            search_id = member_list[0]
        user = User.objects.get(user_id=search_id)
        res = {
            "group_id": self.group_id,
            "type": self.type,
            "name": user.username,
            "member": search_id,
            "icon_address": user.get_user_icon(),
            "member_info": self.get_member_info_list(),
        }
        return res


class MessageEntry(models.Model):
    group = models.ForeignKey(to=BasicGroup, on_delete=models.CASCADE, related_name='group')
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='message_sender')
    type = models.CharField(default='message', max_length=20)  # message & file
    timestamp = models.DateTimeField()
    content = models.TextField()

    def get_message_info(self):
        res = {
            "id": self.id,
            'group_id': self.group_id,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp,
            "raw_timestamp": str(time.mktime(self.timestamp.timetuple())),
            "type": self.type,
            "content": self.content,
        }
        return res
