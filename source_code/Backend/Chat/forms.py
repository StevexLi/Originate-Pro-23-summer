from django import forms

from Chat.models import BasicGroup, GroupChat
from User.models import User


class InviteForm(forms.Form):
    receiver_id = forms.IntegerField(error_messages={
        'required': '此字段是必须的',
    })
    group_id = forms.IntegerField(error_messages={
        'required': '此字段是必须的',
    })
    sender_id = forms.IntegerField()

    def clean(self):
        group_id = self.cleaned_data.get('group_id')
        sender_id = self.cleaned_data.get('sender_id')
        receiver_id = self.cleaned_data.get('receiver_id')
        group_judge = GroupChat.objects.filter(group_id=group_id)
        if not group_judge.exists():
            raise forms.ValidationError('这个群组不存在', code=1005)
        if group_judge[0].type != 'Group':
            raise forms.ValidationError('这个群组不能进行邀请', code=1006)
        if not User.objects.filter(user_id=receiver_id).exists():
            raise forms.ValidationError('接收方不存在', code=1007)
        if group_judge[0].creator_id != sender_id:
            raise forms.ValidationError('权限不够，只有创建者才能进行邀请操作', code=1008)
        return self.cleaned_data


class HistoryForm(forms.Form):
    operator_id = forms.IntegerField()
    group_id = forms.IntegerField(error_messages={
        'required': '此字段是必须的',
    })

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        group_id = self.cleaned_data.get('group_id')
        group_judge = BasicGroup.objects.filter(group_id=group_id)
        if not group_judge.exists():
            raise forms.ValidationError('这个群组不存在', code=1005)
        if operator_id not in group_judge[0].get_member_id_list():
            raise forms.ValidationError('权限不够', code=1006)
        return self.cleaned_data


class CreateGroupForm(forms.Form):
    creator_id = forms.IntegerField()
    name = forms.CharField(max_length=30, error_messages={
        'required': '群聊必须有个名字',
        'max_length': '群聊名不可过长',
    })


class BreakUpForm(forms.Form):
    operator_id = forms.IntegerField()
    group_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        group_id = self.cleaned_data.get('group_id')
        group_judge = GroupChat.objects.filter(group_id=group_id)
        if not group_judge.exists():
            raise forms.ValidationError('这个群组不存在', code=1005)
        if operator_id != group_judge[0].creator.user_id:
            raise forms.ValidationError('权限不够，只有创建者可以删除群组', code=1006)
        return self.cleaned_data


class ExitGroupForm(forms.Form):
    operator_id = forms.IntegerField()
    group_id = forms.IntegerField(error_messages={
        'required': '必须填写群组id'
    })

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        group_id = self.cleaned_data.get('group_id')
        group_judge = GroupChat.objects.filter(id=group_id)
        if not group_judge.exists():
            raise forms.ValidationError('这个群组不存在或不可退出', code=1005)
        if operator_id not in group_judge[0].get_member_id_list():
            raise forms.ValidationError('本身不存在于这个群组中', code=1006)
        return self.cleaned_data
