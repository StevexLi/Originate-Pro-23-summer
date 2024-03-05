from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from Notification.models import GroupNotification
from Backend_Su23.generic_view import MyView
from Utlis.ErrorHandler import get_first_error
from Utlis.RedisUtlis import conn
from .forms import *
from Utlis.LoginUtlis import login_checker
from .models import *


# Create your views here.
@method_decorator(login_checker, name='dispatch')
class GroupInvite(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['sender_id'] = request.user.user_id
        invite_form = InviteForm(data)
        if invite_form.is_valid():
            sender_id = invite_form.cleaned_data.get('sender_id')
            sender = User.objects.get(user_id=sender_id)
            group_id = invite_form.cleaned_data.get('group_id')
            group = GroupChat.objects.get(group_id=group_id)
            content = f"{sender.username}邀请您加入群聊{group.name}"
            announce = GroupNotification.objects.create(sender_id=sender_id,
                                                        receiver_id=invite_form.cleaned_data.get('receiver_id'),
                                                        type='invite', content=content, group_id=group_id)
            announce_dict = {
                'type': 'notification',
                'noti_type': 'invite',
                'data': announce.get_notification_dict(),
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('notification', announce_dict)
            return JsonResponse({
                'code': 0,
                'msg': '邀请消息已发送',
            })
        else:
            err_code, err_msg = get_first_error(invite_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class ExitGroup(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        exit_form = ExitGroupForm(data)
        if exit_form.is_valid():
            group_id = exit_form.cleaned_data.get('group_id')
            operator_id = exit_form.cleaned_data.get('operator_id')
            GroupChat.objects.get(id=group_id).member.get(user_id=operator_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '成功退出此群组',
            })
        else:
            err_code, err_msg = get_first_error(exit_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetHistory(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        history_form = HistoryForm(data)
        if history_form.is_valid():
            group_id = history_form.cleaned_data.get('group_id')
            user_id = request.user.user_id
            res = MessageEntry.objects.filter(group_id=group_id).order_by('-timestamp')
            tmp = []
            msg_num = conn.get(f"group_count_{group_id}_{user_id}", 0)
            for _ in list(res)[:msg_num]:
                tmp.append(_.get_message_info())
            tmp.reverse()
            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': tmp,
            })
        else:
            err_code, err_msg = get_first_error(history_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class CreateGroupChat(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['creator_id'] = request.user.user_id
        create_form = CreateGroupForm(data)
        if create_form.is_valid():
            new_group = GroupChat.objects.create(creator_id=create_form.cleaned_data.get('creator_id'),
                                     name=create_form.cleaned_data.get('name'))
            new_group.member.add(new_group.creator)
            new_group.save()
            return JsonResponse({
                'code': 0,
                'msg': '成功建立群聊',
                'group_id': new_group.group_id,
            })
        else:
            err_code, err_msg = get_first_error(create_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class BreakUpGroup(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        break_up_form = BreakUpForm(data)
        if break_up_form.is_valid():
            group_id = break_up_form.cleaned_data.get('group_id')
            GroupChat.objects.get(group_id=group_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '删除群组成功',
            })
        else:
            err_code, err_msg = get_first_error(break_up_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })
