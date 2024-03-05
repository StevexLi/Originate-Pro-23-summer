from Backend_Su23.celery import app
from .models import BasicNotification


@app.task
def async_process_notification(id_list):
    try:
        for _ in id_list:
            entry = BasicNotification.objects.get(id=_)
            entry.processed = True
            entry.save()
    except Exception as e:
        print(e)


@app.task
def async_delete_notification(id_list):
    try:
        for _ in id_list:
            BasicNotification.objects.get(id=_).delete()
    except Exception as e:
        print(e)






