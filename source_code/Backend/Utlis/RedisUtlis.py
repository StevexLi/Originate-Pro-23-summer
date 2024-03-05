from django.core.cache import caches

conn = caches['default']
vcode_conn = caches['vcode']


def save_vcode(func, email, vcode, time):
    vcode_conn.add(func + ':' + email, vcode, timeout=60 * time)


def check_vcode(func, email, vcode):
    std_vcode = vcode_conn.get(func + ':' + email)
    if std_vcode is None:
        return -2
    else:
        if vcode != std_vcode:
            return -1
        else:
            return 0


def delete_vcode(func, email):
    vcode_conn.delete(func + ':' + email)
