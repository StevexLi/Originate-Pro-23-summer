from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from Backend_Su23.generic_view import MyView
from Chat.models import TeamGroupChat
from Notification.models import TeamNotification
from Utlis.ErrorHandler import get_first_error
from Utlis.FileUtlis import upload_icon
from Utlis.LoginUtlis import login_checker
from .forms import *
from .models import Team
from .tasks import *


# Create your views here.
@method_decorator(login_checker, name='dispatch')
class CreateTeam(MyView):
    def post(self, request):
        flag = False
        creator_id = request.user.user_id
        data = request.POST.copy()
        data['creator_id'] = creator_id
        if request.FILES.get('icon') is not None:
            data['has_icon'] = True
            flag = True
        create_form = CreateTeamForm(data)
        if create_form.is_valid():
            name = create_form.cleaned_data.get('name')
            introduction = create_form.cleaned_data.get('introduction')
            new_team = Team.objects.create(creator_id=creator_id, name=name, introduction=introduction)
            if flag:
                icon = request.FILES.get('icon')
                upload_icon('team/', icon, new_team.id)
            group = TeamGroupChat.objects.create(team=new_team)
            for _ in new_team.get_all_id_list():
                user = User.objects.get(user_id=_)
                group.member.add(user)
            group.save()
            return JsonResponse({
                'code': 0,
                'msg': '创建团队成功',
            })
        else:
            err_code, err_msg = get_first_error(create_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class BreakUpTeam(MyView):
    def post(self, request):
        creator_id = request.user.user_id
        data = request.POST.copy()
        data['creator_id'] = creator_id
        break_form = TeamBreakUpForm(data)
        if break_form.is_valid():
            team_id = break_form.cleaned_data.get('team_id')
            TeamGroupChat.objects.get(team_id=team_id).delete()
            Team.objects.get(id=team_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '解散团队成功'
            })
        else:
            err_code, err_msg = get_first_error(break_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class ChangeAuth(MyView):
    # Allowed Auth operation:
    # 1. admin -> member (creator)
    # 2. member -> admin (creator, admin)
    # 3. delete member (creator, admin)
    # for invite, we shall imply  it in another way.
    def post(self, request):
        operator_id = request.user.user_id
        data = request.POST.copy()
        data['operator_id'] = operator_id
        change_auth_form = ChangeAuthForm(data)
        if change_auth_form.is_valid():
            op_code = change_auth_form.cleaned_data.get('op_code')
            team_id = change_auth_form.cleaned_data.get('team_id')
            user_id = change_auth_form.cleaned_data.get('user_id')
            user = User.objects.get(user_id=user_id)
            team = Team.objects.get(id=team_id)
            match op_code:
                case 1:
                    team.admin.remove(user)
                    team.member.add(user)
                    team.save()
                    res = {'code': 0, 'msg': '权限更改成功'}
                case 2:
                    team.member.remove(user)
                    team.admin.add(user)
                    team.save()
                    res = {'code': 0, 'msg': '权限更改成功'}
                case 3:
                    team.member.remove(user)
                    team.save()
                    tmp = {
                        "sender_id": operator_id,
                        "receiver_id": user_id,
                        "team_id": team_id
                    }
                    async_delete_member.delay(tmp)
                    async_delete_member_from_team_group.delay(team.id, user.user_id)
                    res = {'code': 0, 'msg': '权限更改成功'}
                case _:
                    res = {'code': 1012, 'msg': '无效操作码'}
            return JsonResponse(res)
        else:
            err_code, err_msg = get_first_error(change_auth_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class InviteMember(MyView):
    def post(self, request):
        operator_id = request.user.user_id
        data = request.POST.copy()
        data['operator_id'] = operator_id
        invite_form = InviteForm(data)
        if invite_form.is_valid():
            team = Team.objects.get(id=invite_form.cleaned_data.get('team_id'))
            team_name = team.name
            operator_name = request.user.username
            msg = f"{operator_name}邀请您加入团队{team_name}"
            user_id = User.objects.get(email=invite_form.cleaned_data.get('email')).user_id
            entry = TeamNotification.objects.create(receiver_id=user_id, content=msg,
                                                     sender_id=request.user.user_id,
                                                     team_id=invite_form.cleaned_data.get('team_id'),
                                                     type='invite')
            entry_dict = entry.get_notification_dict()
            entry_dict['team_id'] = team.id
            entry_dict = {
                'type': 'notification',
                'noti_type': 'invite',
                'data': entry_dict,
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('notification', entry_dict)
            return JsonResponse({
                'code': 0,
                'msg': '测试成功',
            })
        else:
            err_code, err_msg = get_first_error(invite_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetInfo(MyView):
    def get(self, request):
        operator_id = request.user.user_id
        data = request.GET.copy()
        data['operator_id'] = operator_id
        get_info_form = GetInfoForm(data)
        if get_info_form.is_valid():
            user_list = []
            team_id = get_info_form.cleaned_data.get('team_id')
            team = Team.objects.get(id=team_id)
            for _ in [team.creator] + list(team.admin.all()) + list(team.member.all()):
                tmp = _.get_user_info_simple()
                if _ == team.creator:
                    tmp['position'] = 'creator'
                elif _ in team.admin.all():
                    tmp['position'] = 'admin'
                else:
                    tmp['position'] = 'member'
                user_list.append(tmp)
            proj_list = []
            proj_set = team.project_set.filter(is_delete=False).all()
            for _ in proj_set:
                proj_list.append(_.get_proj_info())
            res = team.get_team_info_detail()
            res['user_list'] = user_list
            res['project_list'] = proj_list
            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': res,
            })
        else:
            err_code, err_msg = get_first_error(get_info_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class ChangeTeamProfile(MyView):
    def post(self, request):
        user = request.user
        data = request.POST.copy()
        data['operator_id'] = user.user_id
        flag = False
        if request.FILES.get('icon') is not None:
            data['has_icon'] = True
            flag = True
        change_profile_form = ChangeTeamProfileForm(data)
        if change_profile_form.is_valid():
            new_profile = dict(change_profile_form.cleaned_data.items())
            new_profile = {key: value for key, value in new_profile.items() if value != ''}
            team = Team.objects.get(id=change_profile_form.cleaned_data.get('team_id'))
            team_dict = team.get_team_info_detail()
            team_dict.update(new_profile)
            model_form = TeamModelForm(data=team_dict, instance=team)
            model_form.save()
            if flag:
                icon = request.FILES.get('icon')
                upload_icon('team/', icon, team.id)
            return JsonResponse({
                'code': 0,
                'msg': '修改成功',
            })
        else:
            err_code, err_msg = get_first_error(change_profile_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })

