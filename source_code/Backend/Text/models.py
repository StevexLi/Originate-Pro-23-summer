from django.db import models

from User.models import User
from Project.models import Project


# Create your models here.
class Text(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(to=Project, to_field="id", on_delete=models.CASCADE)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=10000)
    is_shared = models.BooleanField(default=False)
    text_url = models.CharField(max_length=100)
    is_write = models.BooleanField(default=False)
class TextHistory(models.Model):
    text_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=10000)
