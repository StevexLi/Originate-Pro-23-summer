from django.http import JsonResponse
from django.utils.decorators import method_decorator
from Backend_Su23.generic_view import MyView
from Utlis.ErrorHandler import get_first_error
from Utlis.FileUtlis import upload_document
from Utlis.LoginUtlis import login_checker
from .forms import *
from .models import Graph

@method_decorator(login_checker, name='dispatch')
class CreateGraph(MyView):
    def post(self, request):
        data = request.POST.copy()
        creator_id = request.user.user_id
        data['creator_id'] = request.user.user_id
        create_form = CreateGraphForm(data)
        if create_form.is_valid():
            name = create_form.cleaned_data.get('name')
            introduction = ''
            content = '{"list":[],"config":{"labelPosition":"left","labelWidth":100,"size":"default","outputHidden":true,"hideRequiredMark":false,"syncLabelRequired":false,"customStyle":""}}'

            project_id = create_form.cleaned_data.get('project_id')
            width = create_form.cleaned_data.get('width')
            Graph.objects.create(creator_id=creator_id, name=name, introduction=introduction, content=content, project_id=project_id, width=width)
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
class DeleteGraph(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        delete_form = DeleteGraphForm(data)
        if delete_form.is_valid():
            graph_id = delete_form.cleaned_data.get('graph_id')
            Graph.objects.get(id=graph_id).delete()
            return JsonResponse({
                'code': 0,
                'msg': '删除原型图成功'
            })
        else:
            err_code, err_msg = get_first_error(delete_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })

@method_decorator(login_checker, name='dispatch')
class SaveGraph(MyView):
    def post(self, request):
        data = request.POST.copy()
        data['operator_id'] = request.user.user_id
        flag = False
        if request.FILES.get('document') is not None:
            data['has_document'] = True
            flag = True
        save_form = SaveGraphForm(data)
        if save_form.is_valid():
            graph_id = save_form.cleaned_data.get('graph_id')
            content = save_form.cleaned_data.get('content')
            width = save_form.cleaned_data.get('width')
            if flag:
                document = request.FILES.get('document')
                upload_document('graph/', document, graph_id)
                Graph.objects.filter(id=graph_id).update(content=content, width=width, has_document = True)
                return JsonResponse({
                    'code': 0,
                    'msg': '保存原型图成功(有)'
                })
            else:
                Graph.objects.filter(id=graph_id).update(content=content,width=width)
                return JsonResponse({
                    'code': 0,
                    'msg': '保存原型图成功(无)'
                })


        else:
            err_code, err_msg = get_first_error(save_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })







@method_decorator(login_checker, name='dispatch')
class GetGraph(MyView):
    def get(self, request):
        data = request.GET.copy()
        data['operator_id'] = request.user.user_id
        get_graph_form = GetGraphForm(data)

        if get_graph_form.is_valid():
            graph_id = get_graph_form.cleaned_data.get('graph_id')
            graph = Graph.objects.get(id=graph_id)
            graph_info = graph.get_graph_info_detail()

            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': graph_info
            })
        else:
            err_code, err_msg = get_first_error(get_graph_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })


class GetGraphs(MyView):
    def get(self, request):
        data = request.GET.copy()
        get_graphs_form = GetGraphsForm(data)

        if get_graphs_form.is_valid():
            project_id = get_graphs_form.cleaned_data.get('project_id')
            graphs = Graph.objects.filter(project_id=project_id)

            res = []
            for graph in graphs:
                res.append(graph.get_graph_info_detail())

            return JsonResponse({
                'code': 0,
                'msg': '查询成功',
                'data': res,
            })
        else:
            err_code, err_msg = get_first_error(get_graphs_form)
            return JsonResponse({
                'code': err_code,
                'msg': err_msg,
            })

