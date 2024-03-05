from django.db import models
from User.models import User
from Team.models import Team
# Create your models here.
class Project(models.Model):
    is_delete = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    create_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, default=1)
    introduction = models.CharField(max_length=60)
    is_shared = models.BooleanField(default=False)

    def get_proj_info(self):
        res = {
            'project_id': self.id,
            'name': self.name,
            'create_date': self.create_date,
            'creator_id': self.creator_id,
            'creator_name': self.creator.username,
            'is_shared': self.is_shared,
        }
        return res




# class RestoredProject(models.Model):
#     name = models.CharField(max_length=30)
#     introduction = models.CharField(max_length=60)
#     create_date = models.DateTimeField()
#     creator = models.ForeignKey(to=User, on_delete=models.CASCADE)

