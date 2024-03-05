from django import forms

from Project.models import Project
from .models import Text


class UploadForm(forms.Form):
    name = forms.CharField(max_length=255, error_messages={
        'required': '文件名不能为空',
        'max_length': '文件名过长',
    })
    creator_id = forms.IntegerField()
    project_id = forms.IntegerField()
    text_url = forms.CharField(max_length=100, error_messages={
        'required': '文件路径不能为空',
        'max_length': '文件路径过长',
    })
    def clean(self):
        creator_id = self.cleaned_data.get('creator_id')
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('文档所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('文档所属项目已被删除', code=1006)
        if not (creator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=creator_id).exists() or
                project_judge[0].team.member.filter(user_id=creator_id).exists()):
            raise forms.ValidationError('权限不足', code=1006)


class DeleteForm(forms.Form):
    text_id = forms.IntegerField(error_messages={
        'required': '此字段不能为空',
    })
    operator_id = forms.IntegerField()

    def clean(self):
        text_id = self.cleaned_data.get('text_id')
        operator_id = self.cleaned_data.get('operator_id')
        text_judge = Text.objects.filter(id=text_id)
        if not text_judge.exists():
            raise forms.ValidationError('不存在此文档', code=1005)
        if text_judge[0].creator_id != operator_id:
            raise forms.ValidationError('只有文档创建人才能删除项目', code=1006)
        return self.cleaned_data


class GetTextsForm(forms.Form):
    operator_id = forms.IntegerField()
    project_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        if not project_judge.exists():
            raise forms.ValidationError('文档所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('文档所属项目已被删除', code=1006)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1006)

        return self.cleaned_data

class GetTextForm(forms.Form):
    project_id = forms.IntegerField()
    text_id = forms.IntegerField()
    def clean(self):
        text_id = self.cleaned_data.get('text_id')
        project_id = self.cleaned_data.get('project_id')
        project_judge = Project.objects.filter(id=project_id)
        text_judge = Text.objects.filter(id=text_id)
        if not project_judge.exists():
            raise forms.ValidationError('文档所属项目不存在', code=1005)
        if project_judge[0].is_delete:
            raise forms.ValidationError('文档所属项目已被删除', code=1006)
        if not text_judge.exists():
            raise forms.ValidationError('不存在此文档', code=1007)

        return self.cleaned_data


class SaveForm(forms.Form):
    text_id = forms.IntegerField(error_messages={
        'required': 'text_id不能为空',
    })
    content = forms.CharField(max_length=10000, error_messages={
        'required': '内容不能为空',
        'max_length': '内容字数过多',
    })
    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })
    operator_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        text_id = self.cleaned_data.get('text_id')
        project_id = self.cleaned_data.get('project_id')
        text_judge = Text.objects.filter(id=text_id)
        project_judge = Project.objects.filter(id=project_id)
        if not text_judge.exists():
            raise forms.ValidationError('文档不存在', code=1005)
        if not project_judge.exists():
            raise forms.ValidationError('文档所属项目不存在', code=1006)
        if project_judge[0].is_delete:
            raise forms.ValidationError('文档所属项目已被删除', code=1007)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1008)
        return self.cleaned_data


class GetHistoryForm(forms.Form):
    text_id = forms.IntegerField(error_messages={
        'required': 'text_id不能为空',
    })

    def clean(self):
        text_id = self.cleaned_data.get('text_id')
        text_judge = Text.objects.filter(id=text_id)
        if not text_judge.exists():
            raise forms.ValidationError('文档不存在', code=1005)
        return self.cleaned_data

class ChangeRoleForm(forms.Form):
    text_id = forms.IntegerField(error_messages={
        'required': 'text_id不能为空',
    })
    project_id = forms.IntegerField(error_messages={
        'required': 'project_id不能为空',
    })
    is_shared = forms.IntegerField(error_messages={
        'required': 'is_shared不能为空',
    })
    is_write = forms.IntegerField(error_messages={
        'required': 'is_write不能为空',
    })
    operator_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        text_id = self.cleaned_data.get('text_id')
        project_id = self.cleaned_data.get('project_id')
        is_shared = self.cleaned_data.get('is_shared')
        is_write = self.cleaned_data.get('is_write')
        text_judge = Text.objects.filter(id=text_id)
        project_judge = Project.objects.filter(id=project_id)
        if not text_judge.exists():
            raise forms.ValidationError('文档不存在', code=1005)
        if not project_judge.exists():
            raise forms.ValidationError('文档所属项目不存在', code=1006)
        if project_judge[0].is_delete:
            raise forms.ValidationError('文档所属项目已被删除', code=1007)
        if is_shared == False and is_write == True:
            raise forms.ValidationError('文档并未被分享', code=1009)
        if not (operator_id == project_judge[0].team.creator_id or
                project_judge[0].team.admin.filter(user_id=operator_id).exists() or
                project_judge[0].team.member.filter(user_id=operator_id).exists()):
            raise forms.ValidationError('权限不足', code=1008)
        return self.cleaned_data