from django.http import JsonResponse
from django.views import View


class MyView(View):
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 1000,
            'msg': '此方法不被允许',
        })
