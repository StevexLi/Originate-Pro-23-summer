from django import forms
from User.models import User


class NotificationForm(forms.Form):
    content = forms.CharField(error_messages={
        'required': '消息必须拥有内容',
    })
    receiver_id = forms.IntegerField(error_messages={
        'required': '接收者不可为空',
    })
    sender_id = forms.IntegerField()
    team_id = forms.IntegerField()

    def clean_receiver_id(self):
        receiver_id = self.cleaned_data.get('receiver_id')
        judge = User.objects.filter(user_id=receiver_id).exists()
        if not judge:
            raise forms.ValidationError('接收方不存在', code=1015)
        return receiver_id


