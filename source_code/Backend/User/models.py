from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

from Utlis.BucketUtlis import bucket
from properties import BUCKET_ROOT


# Create your models here.
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    has_icon = models.BooleanField(default=False)
    introduction = models.CharField(max_length=100, default='这位用户很神秘，还没写下任何介绍')
    phone = models.CharField(max_length=20, default='')
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=3)

    def get_user_info_simple(self):
        res = {'id': self.user_id, 'username': self.username, 'email': self.email,
               'true_name': self.get_full_name(), 'icon_address': self.get_user_icon()}
        return res

    def get_user_info_detail(self):
        res = {'id': self.user_id, 'username': self.username, 'email': self.email, 'true_name': self.get_full_name(),
               'icon_address': self.get_user_icon(), 'gender': self.gender, 'phone': self.phone,
               'introduction': self.introduction}
        return res

    def get_user_info_all(self):
        res = model_to_dict(self)
        return res

    def get_user_info_core(self):
        res = {'id': self.user_id, 'username': self.username, 'icon_address': self.get_user_icon()}
        return res

    def get_user_icon(self):
        if self.has_icon:
            prefix = 'icon/user/' + str(self.user_id)
            name = bucket.list_file(prefix)
            res = BUCKET_ROOT + '/' + name
        else:
            res = BUCKET_ROOT + '/icon/user/default_icon.jpg'
        return 'https://' + res
