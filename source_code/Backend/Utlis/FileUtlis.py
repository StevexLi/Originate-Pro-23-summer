from .BucketUtlis import bucket
import uuid
import os


def save_file(file, uuid, suffix):
    filepath = './media/' + str(uuid) + suffix
    with open(filepath, 'wb') as f:
        for _ in file.chunks():
            f.write(_)
    return filepath


def upload_icon(cat_prefix, icon, user_id):
    try:
        temp_uuid = uuid.uuid1()
        prefix = 'icon/' + cat_prefix + str(user_id)
        key_name = bucket.list_file(prefix)
        if key_name != 'err':
            bucket.delete_file(key_name)
        suffix = os.path.splitext(icon.name)[-1]
        key_name = 'icon/' + cat_prefix + str(user_id) + suffix
        cover_path = save_file(icon, temp_uuid, suffix)
        bucket.upload_file(cover_path, key_name)
        os.remove(cover_path)
    except Exception as e:
        raise e

def upload_document(cat_prefix, document, text_id):
    try:
        temp_uuid = uuid.uuid1()
        prefix = 'documents/' + cat_prefix + str(text_id)
        key_name = bucket.list_file(prefix)
        if key_name != 'err':
            bucket.delete_file(key_name)
        suffix = os.path.splitext(document.name)[-1]
        key_name = 'documents/' + cat_prefix + str(text_id) + suffix
        file_path = save_file(document, temp_uuid, suffix)
        bucket.upload_file(file_path, key_name)
        os.remove(file_path)
    except Exception as e:
        raise e


def delete_document(document_key):
    try:
        bucket.delete_file(document_key)
    except Exception as e:
        raise e
