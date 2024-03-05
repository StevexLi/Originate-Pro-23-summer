import uuid

import jwt
from django.http import JsonResponse

from User.models import User
from Backend_Su23.settings import SECRET_KEY


def generate_jwt(user):
    data = {'id': user.user_id, 'username': user.username, 'jti': str(uuid.uuid1())}
    token = jwt.encode(data, SECRET_KEY)
    return token


def check_jwt(token, request):
    try:
        info = jwt.decode(token, SECRET_KEY, 'HS256')
        judge = User.objects.filter(user_id=info['id'])
        if judge.exists() and judge[0].username == info['username']:
            request.user = judge[0]
            return True
        else:
            raise Exception('Failed!')
    except Exception as e:
        print(e)
        return False


def login_checker(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        res = check_jwt(token, request)
        if not res:
            return JsonResponse({
                'code': 1011,
                'msg': '登录失败',
            })
        else:
            return func(request, *args, **kwargs)
    return wrap
