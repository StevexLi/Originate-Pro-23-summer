from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from Backend_Su23.generic_view import MyView
from Utlis.ErrorHandler import get_first_error
from Utlis.LoginUtlis import login_checker
from .forms import NotificationForm
from .models import BasicNotification


@method_decorator(login_checker, name='dispatch')
class CreateNotification(MyView):
    def post(self, request):
        notification_form = NotificationForm(request.POST)
        if notification_form.is_valid():
            entry = BasicNotification.objects.create(content=notification_form.cleaned_data.get('content'),
                                                     receiver_id=notification_form.cleaned_data.get('receiver_id'),
                                                     sender_id=notification_form.cleaned_data.get('sender_id'),
                                                     team_id=notification_form.cleaned_data.get('team_id'),
                                                     type='normal')
            entry_dict = {
                'type': 'notification',
                'noti_type': 'normal',
                'data': entry.get_notification_dict(),
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('notification', entry_dict)
            return JsonResponse({
                'code': 0,
                'msg': '创建消息完成并转发',
            })

        else:
            err_code, err_msg = get_first_error(notification_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })
