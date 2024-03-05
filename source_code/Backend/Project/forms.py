from django import forms

from Team.models import Team
from .models import Project


class CreateProjectForm(forms.Form):
    name = forms.CharField(max_length=25, error_messages={
        'required': '项目名不可以为空',
        'max_length': '项目名不可以过长',
    })
    creator_id = forms.IntegerField()
    team_id = forms.IntegerField(error_messages={
        'required': '必须填写团队号',
    })
    introduction = forms.CharField(max_length=60)

    def clean(self):
        team_id = self.cleaned_data.get('team_id')
        team_judge = Team.objects.filter(id=team_id)
        if not team_judge.exists():
            raise forms.ValidationError('不存在此团队', code=1005)


class CopyProjectForm(forms.Form):
    project_id = forms.IntegerField()
    name = forms.CharField(max_length=25, error_messages={
        'required': '项目名不可以为空',
        'max_length': '项目名不可以过长',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)


class DeleteProjectForm(forms.Form):
    operator_id = forms.IntegerField()
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        operator_id = self.cleaned_data.get('operator_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)
        if project_judge[0].creator_id != operator_id:
            raise forms.ValidationError('只有项目创建人才能删除项目', code=1006)
        return self.cleaned_data


class RenameProjectForm(forms.Form):
    operator_id = forms.IntegerField()
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })
    name = forms.CharField(max_length=25, error_messages={
        'required': '项目名不可以为空',
        'max_length': '项目名不可以过长',
    })
    introduction = forms.CharField(max_length=60)

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        operator_id = self.cleaned_data.get('operator_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)
        if project_judge[0].creator_id != operator_id:
            raise forms.ValidationError('只有项目创建人才能重命名项目', code=1006)
        return self.cleaned_data

class EmptyProjectForm(forms.Form):
    operator_id = forms.IntegerField()
    team_id = forms.IntegerField()
    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        team_id = self.cleaned_data.get('team_id')
        team_judge = Team.objects.filter(id=team_id)
        if not team_judge.exists():
            raise forms.ValidationError('不存在此团队', code=1005)
        if not (operator_id == team_judge[0].creator_id or
                team_judge[0].admin.filter(user_id=operator_id).exists() or
                team_judge[0].member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('不是团队成员', code=1006)
        return self.cleaned_data




class RestoreProjectForm(forms.Form):
    operator_id = forms.IntegerField()
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        operator_id = self.cleaned_data.get('operator_id')
        restored_project_judge = Project.objects.filter(id=project_id)

        if not restored_project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)

        if not restored_project_judge[0].is_delete:
            raise forms.ValidationError('不能恢复没被删除项目', code=1005)

        if restored_project_judge[0].creator_id != operator_id:
            raise forms.ValidationError('只有项目的创建人才能操作', code=1006)

        return self.cleaned_data


class RemoveProjectForm(forms.Form):
    project_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)
        if not project_judge[0].is_delete:
            raise forms.ValidationError('不能清空没被删除项目', code=1005)
        return self.cleaned_data


class GetinfoForm(forms.Form):
    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })

    def clean(self):
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('不存在此项目', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('项目已被删除', code=1005)
        return self.cleaned_data


class GetDeletelistForm(forms.Form):
    team_id = forms.IntegerField(error_messages={
        'required': 'team_id不能为空',
    })
    operator_id = forms.IntegerField()

    def clean(self):
        team_id = self.cleaned_data.get('team_id')
        operator_id = self.cleaned_data.get('operator_id')
        team_judge = Team.objects.filter(id=team_id)
        if not team_judge.exists():
            raise forms.ValidationError('不存在此团队', code=1005)
        return self.cleaned_data
class ChangeRoleForm(forms.Form):

    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })
    is_shared = forms.IntegerField(error_messages={
        'required': 'is_shared不能为空',
    })
    operator_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)

        if not project_judge.exists():
            raise forms.ValidationError('项目不存在', code=1006)
        if project_judge[0].is_delete:
            raise forms.ValidationError('项目已被删除', code=1007)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1008)
        return self.cleaned_data