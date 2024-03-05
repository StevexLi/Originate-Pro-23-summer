from Backend_Su23.celery import app
from Utlis.RedisUtlis import conn
from .models import MessageEntry


@app.task
def async_backup_message(data):
    MessageEntry.objects.create(sender_id=data['user_id'], content=data['content'],
                                timestamp=data['timestamp'], group_id=data['group_id'])


@app.task
def async_update_count(group_id):
    in_room_member_id_list = conn.get(f"group_{group_id}_chat_member")
    all_member_id_list = conn.get(f"group_{group_id}_chat_all_member")
    for _ in in_room_member_id_list:
        name = f"group_count_{group_id}_{_}"
        conn.set(name, 0, timeout=None)
    for _ in [uid for uid in all_member_id_list if uid not in in_room_member_id_list]:
        name = f"group_count_{group_id}_{_}"
        conn.add(name, 0, timeout=None)
        conn.incr(name)
