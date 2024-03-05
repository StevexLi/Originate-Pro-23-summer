from django.http import JsonResponse
from django.utils.decorators import method_decorator
from Backend_Su23.generic_view import MyView
from Chat.models import BasicGroup, GroupChat, PrivateChat, TeamGroupChat
from Utlis.FileUtlis import upload_icon
from .forms import *
from Utlis.ErrorHandler import get_first_error
from Utlis.LoginUtlis import generate_jwt, login_checker
from .models import User
from .tasks import *
from Team.models import Team


# Create your views here.
class Register(MyView):
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password_1']
            email = register_form.cleaned_data['email']
            User.objects.create_user(username, email, password)
            async_send_response_to_mail.delay('Register', email)
            return JsonResponse({
                'code': '0',
                'msg': '注册成功',
            })
        else:
            err_code, err_msg = get_first_error(register_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


class Login(MyView):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = User.objects.get(username=login_form.cleaned_data.get('username'))
            token = generate_jwt(user)
            return JsonResponse({
                'code': 0,
                'msg': '登录成功',
                'token': token,
            })
        else:
            err_code, err_msg = get_first_error(login_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


class SendVcode(MyView):
    def post(self, request):
        email_form = EmailVcodeForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            func = email_form.cleaned_data.get('func')
            async_send_vcode_to_mail.delay(func, email)
            return JsonResponse({
                'code': 0,
                'msg': '验证码发送成功',
            })
        else:
            err_code, err_msg = get_first_error(email_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


class FindPassword(MyView):
    def post(self, request):
        check_form = FindPasswordForm(request.POST)
        if check_form.is_valid():
            email = check_form.cleaned_data.get('email')
            password = check_form.cleaned_data.get('password_1')
            func = 'Find_Password'
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            async_send_response_to_mail.delay(func, email)
            return JsonResponse({
                'code': 0,
                'msg': '成功',
            })
        else:
            err_code, err_msg = get_first_error(check_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class ChangeProfile(MyView):
    def post(self, request):
        data = request.POST.copy()
        user_id = request.user.user_id
        data['user_id'] = request.user.user_id
        flag = False
        if request.FILES.get('icon') is not None:
            data['has_icon'] = True
            flag = True
        change_profile_form = ChangeProfileForm(data)
        if change_profile_form.is_valid():
            new_profile = dict(change_profile_form.cleaned_data.items())
            new_profile = {key: value for key, value in new_profile.items() if value != ''}
            user = User.objects.get(user_id=user_id)
            user_dict = user.get_user_info_all()
            user_dict.update(new_profile)
            model_form = UserModelForm(data=user_dict, instance=user)
            model_form.save()
            if flag:
                icon = request.FILES.get('icon')
                upload_icon('user/', icon, user_id)
            return JsonResponse({
                'code': 0,
                'msg': '测试',
            })
        else:
            err_code, err_msg = get_first_error(change_profile_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetUserInfo(MyView):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        if user_id is None:
            res = request.user.get_user_info_detail()
        else:
            try:
                res = User.objects.get(user_id=user_id).get_user_info_detail()
            except Exception:
                return JsonResponse({
                    'code': 1013,
                    'msg': '用户不存在',
                })
        return JsonResponse({
            'code': 0,
            'msg': '查询成功',
            'data': res,
        })


@method_decorator(login_checker, name='dispatch')
class GetAllTeam(MyView):
    def get(self, request):
        admin_set = Team.objects.filter(admin=request.user)
        member_set = Team.objects.filter(member=request.user)
        creator_set = Team.objects.filter(creator=request.user)
        res = []
        for _ in list(creator_set) + list(admin_set) + list(member_set):
            res.append(_.get_team_info_detail())
        return JsonResponse({
            'code': 0,
            'msg': '查询完成',
            'data': res,
        })


@method_decorator(login_checker, name='dispatch')
class GetAllGroup(MyView):
    def get(self, request):
        res_1 = TeamGroupChat.objects.filter(member=request.user)
        res_2 = GroupChat.objects.filter(member=request.user)
        res_3 = PrivateChat.objects.filter(member=request.user)
        res_list = []
        for _ in list(res_1) + list(res_2) + list(res_3):
            res_list.append(_.get_group_info(user_id=request.user.user_id))
        return JsonResponse({
            'code': 0,
            'msg': '查询完成',
            'data': res_list,
        })


class CheckInTeam(MyView):
    def get(self, request):
        team_id = request.GET.get('team_id')
        user_id = request.GET.get('user_id')
        team = Team.objects.get(id=team_id)
        if user_id in team.get_all_id_list():
            res = True
        else:
            res = False
        return JsonResponse({
            'code': 0,
            'msg': '查询完成',
            'data': res,
        })
