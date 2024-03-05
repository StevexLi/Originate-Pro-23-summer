from django.db import models

from Project.models import Project
from User.models import User
from Utlis.BucketUtlis import bucket
from properties import BUCKET_ROOT


# Create your models here.
class Graph(models.Model):
    name = models.CharField(max_length=30)
    project = models.ForeignKey(to=Project, to_field="id", on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    create_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=60)
    width = models.IntegerField(default=800, blank=True, null=True)
    has_document = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

    def get_graph_info_detail(self):
        res = {'graph_id': self.id, 'name': self.name, 'project_id': self.project.id,
               'creator': self.creator.get_user_info_simple(),
               'content': self.content, 'create_date': self.create_date, 'file_address': self.get_graph_document(),
               'width': self.width,
               'introduction': self.introduction, 'has_file': self.has_document, 'is_shared': self.is_shared}
        return res

    def get_graph_document(self):
        if self.has_document:
            prefix = 'documents/graph/' + str(self.id)
            name = bucket.list_file(prefix)
            res = BUCKET_ROOT + '/' + name
        else:
            res = BUCKET_ROOT + '/documents/graph/default_graph.jpg'
        return 'https://' + res
