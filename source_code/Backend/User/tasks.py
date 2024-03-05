from Backend_Su23.celery import app
from Utlis.MailUtlis import send_vcode_to_mail, send_response_to_mail


@app.task
def async_send_vcode_to_mail(func, email, time=5):
    send_vcode_to_mail(func, email, time)


@app.task
def async_send_response_to_mail(func, email):
    send_response_to_mail(func, email)
