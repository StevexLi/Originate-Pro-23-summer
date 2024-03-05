import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from Backend_Su23.generic_view import MyView
from Utlis.ErrorHandler import get_first_error
from Utlis.LoginUtlis import login_checker
from .forms import *
from .models import Text, TextHistory


@method_decorator(login_checker, name='dispatch')
class CreateText(MyView):
    def post(self, request):
        data = request.POST.copy()
        creator_id = request.user.user_id
        data['creator_id'] = request.user.user_id
        upload_form = UploadForm(data)
        if upload_form.is_valid():
            name = upload_form.cleaned_data.get('name')
            project_id = upload_form.cleaned_data.get('project_id')
            text_url = upload_form.cleaned_data.get('text_url')
            content = ""
            Text.objects.create(name=name, content=content, creator_id=creator_id, project_id=project_id,
                                text_url=text_url)

            return JsonResponse({
                'code': 0,
                'msg': '创建成功',
            })
        else:
            err_code, err_msg = get_first_error(upload_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


# @method_decorator(login_checker, name='dispatch')
# class CreateText(MyView):
#     def post(self, request):
#         data = request.POST.copy()
#         creator_id = request.user.user_id
#         data['creator_id'] = request.user.user_id
#         upload_form = UploadForm(data)
#
#         if upload_form.is_valid():
#             name = upload_form.cleaned_data.get('name')
#             project_id = upload_form.cleaned_data.get('project_id')
#             content = ""
#             text = Text.objects.create(name=name, content=content, creator_id=creator_id, project_id=project_id)
#
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 f"text_{text.id}",
#                 {
#                     'type': 'send.text_content',
#                     'content': content,
#                     'user_id': request.user.user_id,
#                     'project_id': project_id,
#                     'name': name,
#                 }
#             )
#             return JsonResponse({
#                 'code': 0,
#                 'msg': '创建成功',
#             })
#         else:
#             err_code, err_msg = get_first_error(upload_form)
#             return JsonResponse({
#                 'code': err_code,
#                 'msg': err_msg,
#             })


@method_decorator(login_checker, name='dispatch')
class DeleteText(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        delete_form = DeleteForm(data)

        if delete_form.is_valid():
            text_id = delete_form.cleaned_data.get('text_id')
            text = Text.objects.get(id=text_id)
            text.delete()
            return JsonResponse({
                'code': 0,
                'msg': '删除成功',
            })


        else:
            err_code, err_msg = get_first_error(delete_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetTexts(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        get_texts_form = GetTextsForm(data)

        if get_texts_form.is_valid():
            project_id = get_texts_form.cleaned_data.get('project_id')
            texts = Text.objects.filter(project_id=project_id)

            res = []
            pattern = r'1\w+'
            for text in texts:
                if re.match(pattern, text.text_url):
                    continue
                res.append({
                    'text_id': text.id,
                    'name': text.name,
                    'text_url': text.text_url,
                    'creator': text.creator.get_user_info_simple(),

                })

            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': res,
            })
        else:
            err_code, err_msg = get_first_error(get_texts_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


class GetText(MyView):
    def get(self, request):
        data = request.GET.copy()
        get_text_form = GetTextForm(data)

        if get_text_form.is_valid():
            text_id = get_text_form.cleaned_data.get('text_id')
            try:
                text = Text.objects.get(id=text_id)
            except Text.DoesNotExist:
                return JsonResponse({
                    'code': 1008,
                    'msg': '其他错误',
                })
            pattern = r'1\w+'
            if re.match(pattern, text.text_url):
                return JsonResponse({
                    'code': 1007,
                    'msg': '非文档',
                })
            text_info = {
                'name': text.name,
                'content': text.content,
                'text_url': text.text_url,
                'is_shared': text.is_shared,
                'is_write': text.is_write,
                'creator': text.creator.get_user_info_simple(),
            }

            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': text_info,
            })

        else:
            err_code, err_msg = get_first_error(get_text_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class SaveText(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        save_form = SaveForm(data)
        if save_form.is_valid():
            text_id = save_form.cleaned_data.get('text_id')
            content = save_form.cleaned_data.get('content')
            Text.objects.filter(id=text_id).update(content=content)
            TextHistory.objects.create(text_id=text_id, content=content)
            return JsonResponse({
                'code': 0,
                'msg': '保存成功',
            })
        else:
            err_code, err_msg = get_first_error(save_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetHistory(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        get_history_form = GetHistoryForm(data)

        if get_history_form.is_valid():
            text_id = get_history_form.cleaned_data.get('text_id')
            try:
                history_texts = TextHistory.objects.filter(text_id=text_id)
            except TextHistory.DoesNotExist:
                return JsonResponse({
                    'code': 1008,
                    'msg': '没有该文档历史版本',
                })

            res = []
            for history in history_texts:
                res.append({
                    'id': history.id,
                    'text_id': history.text_id,
                    'content': history.content,
                    'create_date': history.create_date,
                })

            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': res,
            })

        else:
            err_code, err_msg = get_first_error(get_history_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class ChangeRole(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        change_role_form = ChangeRoleForm(data)
        if change_role_form.is_valid():
            text_id = change_role_form.cleaned_data.get('text_id')
            is_shared = change_role_form.cleaned_data.get('is_shared')
            is_write = change_role_form.cleaned_data.get('is_write')
            Text.objects.filter(id=text_id).update(is_shared=is_shared, is_write=is_write)
            return JsonResponse({
                'code': 0,
                'msg': '更改成功',
            })
        else:
            err_code, err_msg = get_first_error(change_role_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })
