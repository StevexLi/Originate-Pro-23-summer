import re

from django import forms
from Utlis.RedisUtlis import check_vcode

from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3, error_messages={
        'required': '用户名不可以为空',
        'min_length': '用户名过短',
        'max_length': '用户名过长',
    })
    password_1 = forms.CharField(max_length=50, min_length=8, error_messages={
        'required': '密码不可以为空',
        'min_length': '密码不可以过短',
        'max_length': '密码不可以过长',
    })
    password_2 = forms.CharField()
    email = forms.EmailField(error_messages={
        'required': '必须填写电子邮箱',
        'invalid': '电子邮箱格式不对',
    })
    vcode = forms.CharField(error_messages={
        'required': '必须填写验证码',
    })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_judge1 = User.objects.filter(username=username).exists()
        if username_judge1:
            raise forms.ValidationError('用户名已存在', code=1005)
        username_judge2 = re.fullmatch("[A-Za-z0-9_\u4e00-\u9fa5\u0800-\u4e00]{3,30}", username)
        if not username_judge2:
            raise forms.ValidationError('用户名不符合命名规范', code=1006)
        return username

    def clean_password_1(self):
        password_1 = self.cleaned_data.get('password_1')
        password_judge1 = re.fullmatch("[A-Za-z0-9_]{8,30}", password_1)
        if not password_judge1:
            raise forms.ValidationError('密码不符合规范', code=1007)
        return password_1

    def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 != password_2:
            raise forms.ValidationError('两次密码输入不一致', code=1008)
        return password_2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_judge = User.objects.filter(email=email)
        if email_judge.exists():
            raise forms.ValidationError('此邮箱已经被注册', code=1011)
        return email

    def clean_vcode(self):
        vcode = self.cleaned_data.get('vcode')
        email = self.cleaned_data.get('email')
        func = 'Register'
        if email is None or check_vcode(func, email, vcode) != 0:
            raise forms.ValidationError('验证失败', code=1009)
        return vcode


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={
        'required': '用户名不可以为空',
    })
    password = forms.CharField(error_messages={
        'required': '密码不可以为空',
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_judge = User.objects.filter(username=username)
        if not user_judge.exists():
            raise forms.ValidationError('不存在此用户', code=1001)
        passwd_judge = user_judge[0].check_password(password)
        if not passwd_judge:
            raise forms.ValidationError('密码错误', code=1002)
        return self.cleaned_data


class EmailVcodeForm(forms.Form):
    email = forms.EmailField(error_messages={
        "required": '电子邮箱不可以为空',
        "invalid": '电子邮箱格式错误',
    })
    func = forms.CharField(error_messages={
        'required': '此字段不可以为空'
    })


class FindPasswordForm(forms.Form):
    email = forms.EmailField(error_messages={
        'required': '必须填写电子邮箱',
        'invalid': '电子邮箱格式不对',
    })
    password_1 = forms.CharField(max_length=50, min_length=8, error_messages={
        'required': '密码不可以为空',
        'min_length': '密码不可以过短',
        'max_length': '密码不可以过长',
    })
    password_2 = forms.CharField()
    vcode = forms.CharField()

    def clean_password_1(self):
        password_1 = self.cleaned_data.get('password_1')
        password_judge1 = re.fullmatch("[A-Za-z0-9_]{8,30}", password_1)
        if not password_judge1:
            raise forms.ValidationError('密码不符合规范', code=1007)
        return password_1

    def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 != password_2:
            raise forms.ValidationError('两次密码输入不一致', code=1008)
        return password_2

    def clean_vcode(self):
        vcode = self.cleaned_data.get('vcode')
        email = self.cleaned_data.get('email')
        func = 'Find_Password'
        if check_vcode(func, email, vcode) != 0:
            raise forms.ValidationError('验证失败', code=1010)
        return vcode


class ChangeProfileForm(forms.Form):
    user_id = forms.IntegerField()
    username = forms.CharField(max_length=30, min_length=3, required=False, error_messages={
        'min_length': '用户名过短',
        'max_length': '用户名过长',
    })
    first_name = forms.CharField(max_length=12, required=False, error_messages={
        'max_length': '不支持过长的姓',
    })
    last_name = forms.CharField(max_length=20, required=False, error_messages={
        'max_length': '不支持过长的名',
    })
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], error_messages={
        'required': '此字段是必要的',
    })
    phone = forms.CharField(min_length=7, max_length=20, required=False, error_messages={
        'min_length': '此电话号码过短',
        'max_length': '此电话号码过长',
    })
    introduction = forms.CharField(max_length=50, min_length=1, required=False, error_messages={
        'min_length': '不允许提交空简介',
        'max_length': '不能提交过长的简介',
    })
    has_icon = forms.BooleanField(required=False)

    def clean_username(self):
        if not self.fields['username'].required:
            return ''
        user_id = self.cleaned_data.get('user_id')
        username = self.cleaned_data.get('username')
        ori_username = User.objects.get(user_id=user_id).username
        username_judge1 = User.objects.filter(username=username).exists()
        if username != ori_username and username_judge1:
            raise forms.ValidationError('用户名已存在', code=1005)
        username_judge2 = re.fullmatch("[A-Za-z0-9_\u4e00-\u9fa5\u0800-\u4e00]{3,30}", username)
        if not username_judge2:
            raise forms.ValidationError('用户名不符合命名规范', code=1006)
        return username


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'phone', 'introduction', 'has_icon']






