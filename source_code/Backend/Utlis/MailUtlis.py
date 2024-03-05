import random
from django.core.mail import send_mail
from Utlis.RedisUtlis import save_vcode, delete_vcode


def generate_vcode():
    vcode = random.randint(0, 999999)
    vcode = str(vcode)
    return vcode.zfill(6)


def send_vcode_to_mail(func, dest_email, time):
    vcode = generate_vcode()
    send_mail(
        subject='验证码测试',
        message='您好，您的验证码是 ' + vcode + ' ,验证码有效期为' + str(time) + '分钟',
        from_email='django_backend@163.com',
        recipient_list=[dest_email]
    )
    save_vcode(func, dest_email, vcode, time)


def send_response_to_mail(func, dest_email):
    delete_vcode(func, dest_email)
    send_mail(
        subject='验证成功',
        message=f'您好，您的{func}操作已经完成！',
        from_email='django_backend@163.com',
        recipient_list=[dest_email]
    )
