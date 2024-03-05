from django.http import JsonResponse
from django.utils.decorators import method_decorator
from Backend_Su23.generic_view import MyView
from Graph.models import Graph
from Text.models import Text
from Utlis.ErrorHandler import get_first_error
from Utlis.LoginUtlis import login_checker
from .forms import *
from .models import Project


# Create your views here.
@method_decorator(login_checker, name='dispatch')
class CreateProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        creator_id = request.user.user_id
        data['creator_id'] = request.user.user_id
        create_form = CreateProjectForm(data)
        if create_form.is_valid():
            name = create_form.cleaned_data.get('name')
            team_id = create_form.cleaned_data.get('team_id')
            introduction = create_form.cleaned_data.get('introduction')
            Project.objects.create(creator_id=creator_id, name=name, team_id=team_id, introduction=introduction)
            return JsonResponse({
                'code': 0,
                'msg': '创建成功',
            })
        else:
            err_code, err_msg = get_first_error(create_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })



@method_decorator(login_checker, name='dispatch')
class CopyProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        creator_id = request.user.user_id
        data['creator_id'] = request.user.user_id
        copy_form = CopyProjectForm(data)
        if copy_form.is_valid():
            name = copy_form.cleaned_data.get('name')
            project_id = copy_form.cleaned_data.get('project_id')
            project = Project.objects.filter(id=project_id)
            project_id = project[0].id
            creator_id = project[0].creator_id
            team_id = project[0].team_id
            introduction = project[0].introduction
            is_shared = project[0].is_shared
            copy_project = Project.objects.create(creator_id=creator_id, name=name, team_id=team_id,
                                                  introduction=introduction, is_shared=is_shared)
            copy_project_id = copy_project.id
            texts = Text.objects.filter(project_id=project_id)
            graphs = Graph.objects.filter(project_id=project_id)
            for text in texts:
                text_name = text.name
                text_content = text.content
                text_creator_id = text.creator_id
                text_project_id = copy_project_id
                text_url = text.text_url
                text_is_write = text.is_write
                text_is_shared = text.is_shared
                Text.objects.create(name=text_name, content=text_content, creator_id=text_creator_id, project_id=text_project_id,
                                    text_url=text_url, is_shared=text_is_shared, is_write=text_is_write)

            for graph in graphs:
                graph_name = graph.name
                graph_content = graph.content
                graph_creator_id = graph.creator_id
                graph_project_id = copy_project_id
                graph_width = graph.width
                graph_introduction = graph.introduction
                graph_is_shared = graph.is_shared
                graph_has_document = graph.has_document
                Graph.objects.create(creator_id=graph_creator_id, name=graph_name, introduction=graph_introduction, content=graph_content,
                                     project_id=graph_project_id, width=graph_width, is_shared=graph_is_shared, has_document=graph_has_document)

            return JsonResponse({
                'code': 0,
                'msg': '创建副本成功',
            })
        else:
            err_code, err_msg = get_first_error(copy_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })






@method_decorator(login_checker, name='dispatch')
class DeleteProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        delete_form = DeleteProjectForm(data)

        if delete_form.is_valid():
            project_id = delete_form.cleaned_data.get('project_id')

            Project.objects.filter(id=project_id).update(is_delete=True)

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


# @method_decorator(login_checker, name='dispatch')
# class DeleteProject(MyView):
#     def post(self, request):
#         data = request.POST.copy()
#         data['operator_id'] = request.user.user_id
#         delete_form = DeleteProjectForm(data)
#         if delete_form.is_valid():
#             Project.objects.get(id=delete_form.cleaned_data.get('project_id')).delete()
#             return JsonResponse({
#                 'code': 0,
#                 'msg': '删除成功',
#             })
#         else:
#             err_code, err_msg = get_first_error(delete_form)
#             return JsonResponse({
#                 'code': err_code,
#                 'msg': err_msg,
#             })


@method_decorator(login_checker, name='dispatch')
class UpdateProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        rename_form = RenameProjectForm(data)
        if rename_form.is_valid():
            project = Project.objects.get(id=rename_form.cleaned_data.get('project_id'))
            if project.is_delete:
                return JsonResponse({
                    'code': 1008,
                    'msg': '项目已被删除',
                })

            project.name = rename_form.cleaned_data.get('name')
            project.introduction = rename_form.cleaned_data.get('introduction')
            project.save()
            return JsonResponse({
                'code': 0,
                'msg': '重命名成功',
            })
        else:
            err_code, err_msg = get_first_error(rename_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class RestoreProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        restore_form = RestoreProjectForm(data)

        if restore_form.is_valid():
            project_id = restore_form.cleaned_data.get('project_id')
            Project.objects.filter(id=project_id).update(is_delete=False)
            return JsonResponse({
                'code': 0,
                'msg': '恢复成功',
            })

        else:
            err_code, err_msg = get_first_error(restore_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class RemoveProject(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        remove_form = RemoveProjectForm(data)
        if remove_form.is_valid():
            project_id = remove_form.cleaned_data.get('project_id')

            Project.objects.filter(id=project_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '永久删除完成',
            })
        else:
            err_code, err_msg = get_first_error(remove_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class EmptyRecycleBin(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        empty_form = EmptyProjectForm(data)
        if empty_form.is_valid():
            team_id = empty_form.cleaned_data.get('team_id')
            Project.objects.filter(is_delete=True,team_id=team_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '回收站已清空',
            })
        else:
            err_code, err_msg = get_first_error(empty_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class Getinfo(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        getinfo_form = GetinfoForm(data)
        if getinfo_form.is_valid():
            project_id = getinfo_form.cleaned_data.get('project_id')
            project = Project.objects.filter(id=project_id)
            graphs = Graph.objects.filter(project_id=project_id)
            texts = Text.objects.filter(project_id=project_id)

            graph_list = []
            for graph in graphs:
                graph_list.append(
                    graph.get_graph_info_detail()
                )

            text_list = []
            for text in texts:
                text_list.append({
                    'text_id': text.id,
                    'name': text.name,
                    'text_url': text.text_url,
                    'creator': text.creator.get_user_info_simple()
                })

            return JsonResponse({
                'code': 0,
                'msg': '获取信息成功',
                'data': {
                    'name': project[0].name,
                    'team_id': project[0].team.id,
                    'team_name': project[0].name,
                    'is_shared': project[0].is_shared,
                    'creator': project[0].creator.get_user_info_simple(),
                    'create_date': project[0].create_date,
                    'introduction': project[0].introduction,
                    'graph_list': graph_list,
                    'text_list': text_list,
                },

            })
        else:
            err_code, err_msg = get_first_error(getinfo_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


@method_decorator(login_checker, name='dispatch')
class GetDeletelist(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        get_delete_list_form = GetDeletelistForm(data)
        if get_delete_list_form.is_valid():
            team_id = get_delete_list_form.cleaned_data.get('team_id')
            deleted_projects = Project.objects.filter(team_id=team_id, is_delete=True)

            res = []
            for deleted_project in deleted_projects:
                res.append(deleted_project.get_proj_info())
            return JsonResponse({
                'code': 0,
                'msg': '获取信息成功',
                'data': {
                    'deleted_projects': res,
                },
            })
        else:
            err_code, err_msg = get_first_error(get_delete_list_form)
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
            project_id = change_role_form.cleaned_data.get('project_id')
            is_shared = change_role_form.cleaned_data.get('is_shared')
            Project.objects.filter(id=project_id).update(is_shared=is_shared)
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
