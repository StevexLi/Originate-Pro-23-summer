from django import forms

from Project.models import Project
from .models import Graph


class CreateGraphForm(forms.Form):
    name = forms.CharField(max_length=25, error_messages={
        'required': '原型图名不可以为空',
        'max_length': '原型图名不可以过长',
    })
    creator_id = forms.IntegerField()
    project_id = forms.IntegerField()
    width = forms.IntegerField()

    def clean(self):
        creator_id = self.cleaned_data.get('creator_id')
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('原型图所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('原型图所属项目已被删除', code=1006)
        if not (creator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=creator_id).exists() or
                project_judge[0].team.member.filter(user_id=creator_id).exists()):
            raise forms.ValidationError('权限不足', code=1006)


class DeleteGraphForm(forms.Form):
    operator_id = forms.IntegerField()
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })
    graph_id = forms.IntegerField()
    def clean(self):
        graph_id = self.cleaned_data.get('graph_id')
        operator_id = self.cleaned_data.get('operator_id')
        project_id = self.cleaned_data.get('project_id')
        graph_judge = Graph.objects.filter(id=graph_id)
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('原型图所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('原型图所属项目已被删除', code=1006)
        if not graph_judge.exists():
            raise forms.ValidationError('不存在此原型图', code=1005)
        if graph_judge[0].creator_id != operator_id:
            raise forms.ValidationError('只有项目创建人才能删除原型图', code=1006)
        return self.cleaned_data





class GetGraphForm(forms.Form):
    operator_id = forms.IntegerField()
    graph_id = forms.IntegerField(error_messages={
        'required': 'graph_id不能为空',
    })
    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        graph_id = self.cleaned_data.get('graph_id')
        project_id = self.cleaned_data.get('project_id')
        graph_judge = Graph.objects.filter(id=graph_id)
        project_judge = Project.objects.filter(id=project_id)

        if not project_judge.exists():
            raise forms.ValidationError('原型图所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('原型图所属项目已被删除', code=1006)
        if not graph_judge.exists():
            raise forms.ValidationError('不存在此原型图', code=1007)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1008)

        return self.cleaned_data


class GetGraphsForm(forms.Form):
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('原型图所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('原型图所属项目已被删除', code=1006)
        if not project_judge[0].is_shared:
            raise forms.ValidationError('权限不足', code=1008)

        return self.cleaned_data


class SaveGraphForm(forms.Form):
    graph_id = forms.IntegerField(error_messages={
        'required': 'graph_id不能为空',
    })
    content = forms.CharField(max_length=10000, error_messages={
        'required': '内容不能为空',
        'max_length': '内容字数过多',
    })
    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })
    operator_id = forms.IntegerField()
    width = forms.IntegerField(error_messages={
        'required': 'width不能为空',
    })

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        graph_id = self.cleaned_data.get('graph_id')
        project_id = self.cleaned_data.get('project_id')
        graph_judge = Graph.objects.filter(id=graph_id)
        project_judge = Project.objects.filter(id=project_id)
        if not graph_judge.exists():
            raise forms.ValidationError('原型图不存在', code=1005)
        if not project_judge.exists():
            raise forms.ValidationError('原型图所属项目不存在', code=1006)
        if project_judge[0].is_delete:
            raise forms.ValidationError('原型图所属项目已被删除', code=1007)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1008)

        return self.cleaned_data
