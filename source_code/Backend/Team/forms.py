from django import forms
from .models import Team
from User.models import User


class CreateTeamForm(forms.Form):
    creator_id = forms.IntegerField()
    name = forms.CharField(max_length=20, error_messages={
        'required': '团队名不可为空',
        'max_length': '团队名不能过长',
    })
    introduction = forms.CharField(required=False)


class TeamBreakUpForm(forms.Form):
    creator_id = forms.IntegerField()
    team_id = forms.IntegerField()

    def clean(self):
        team = Team.objects.filter(id=self.cleaned_data.get('team_id'))
        if not team.exists():
            raise forms.ValidationError('不存在此团队', code=1001)
        if team[0].creator_id != self.cleaned_data.get('creator_id'):
            raise forms.ValidationError('权限不够，只有创建者可以解散该团队', code=1002)
        return self.cleaned_data


class ChangeAuthForm(forms.Form):
    operator_id = forms.IntegerField()
    user_id = forms.IntegerField()
    team_id = forms.IntegerField()
    op_code = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        team_id = self.cleaned_data.get('team_id')
        op_code = self.cleaned_data.get('op_code')
        user_id = self.cleaned_data.get('user_id')
        team = Team.objects.filter(id=team_id)
        user = User.objects.filter(user_id=user_id)
        if not user.exists():
            raise forms.ValidationError('不存在此用户', code=1003)
        if not team.exists():
            raise forms.ValidationError('不存在此团队', code=1001)
        if (operator_id not in team[0].get_auth_id_list()) or \
                (op_code == 1 and operator_id != team[0].creator_id):
            raise forms.ValidationError('权限不足', code=1002)
        return self.cleaned_data


class InviteForm(forms.Form):
    operator_id = forms.IntegerField()
    team_id = forms.IntegerField()
    email = forms.EmailField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        team_id = self.cleaned_data.get('team_id')
        email = self.cleaned_data.get('email')
        team = Team.objects.filter(id=team_id)
        if not team.exists():
            raise forms.ValidationError('不存在此团队', code=1001)
        if operator_id not in team[0].get_auth_id_list():
            raise forms.ValidationError('权限不足', code=1002)
        user = User.objects.filter(email=email)
        if not user.exists():
            raise forms.ValidationError('此邮箱未绑定用户', code=1003)
        if user[0].user_id in team[0].get_all_id_list():
            raise forms.ValidationError('此用户已经在团队中', code=1004)
        return self.cleaned_data


class GetInfoForm(forms.Form):
    operator_id = forms.IntegerField()
    team_id = forms.IntegerField()

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        team_id = self.cleaned_data.get('team_id')
        team = Team.objects.filter(id=team_id)
        if not team.exists():
            raise forms.ValidationError('不存在此团队', code=1001)
        if operator_id not in team[0].get_all_id_list():
            raise forms.ValidationError('权限不足', code=1002)
        return self.cleaned_data


class ChangeTeamProfileForm(forms.Form):
    operator_id = forms.IntegerField()
    team_id = forms.IntegerField(error_messages={
        'required': '必须要有团队号',
    })
    introduction = forms.CharField(required=False)
    name = forms.CharField(required=False, max_length=20, error_messages={
        'max_length': '团队名不能过长',
    })
    has_icon = forms.BooleanField(required=False)

    def clean(self):
        operator_id = self.cleaned_data.get('operator_id')
        team = Team.objects.filter(id=self.cleaned_data.get('team_id'))
        if not team.exists():
            raise forms.ValidationError('不存在此团队', code=1001)
        if operator_id not in team[0].get_auth_id_list():
            raise forms.ValidationError('权限不足', code=1002)
        return self.cleaned_data


class TeamModelForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'introduction', 'has_icon']
