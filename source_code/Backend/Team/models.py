from django.db import models

from User.models import User
from properties import BUCKET_ROOT
from Utlis.BucketUtlis import bucket


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=20)
    introduction = models.CharField(max_length=60)
    has_icon = models.BooleanField(default=False)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='creator')
    admin = models.ManyToManyField(to=User, related_name='admin')
    member = models.ManyToManyField(to=User, related_name='member')

    def get_auth_id_list(self):
        res = [self.creator_id]
        for admin in self.admin.all():
            res.append(admin.user_id)
        return res

    def get_all_id_list(self):
        res = self.get_auth_id_list()
        for _ in self.member.all():
            res.append(_.user_id)
        return res

    def get_team_info_detail(self):
        res = {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'icon_address': self.get_icon(),
        }
        return res

    def get_icon(self):
        if self.has_icon:
            prefix = 'icon/team/' + str(self.id)
            name = bucket.list_file(prefix)
            res = BUCKET_ROOT + '/' + name
        else:
            res = BUCKET_ROOT + '/icon/team/default_icon.jpg'
        return 'https://' + res

