from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from properties import *


# oss的控制类，需要能创建存储，初始化存储，上传，下载，删除，同时要有审核功能
class Bucket:
    proxies = {
        'http': '127.0.0.1:80',
        'https': '127.0.0.1:443'
    }

    def __init__(self, secret_id, secret_key, bucket_name, region, token=None):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.region = region
        self.token = token
        self.scheme = 'https'
        self.config = CosConfig(Region=self.region, Token=self.token, SecretId=self.secret_id,
                                SecretKey=self.secret_key, Scheme=self.scheme)
        self.client = CosS3Client(self.config)

    # 文件操作类
    def upload_file(self, local_file, key_name):
        try:
            self.client.upload_file(
                Bucket=self.bucket_name,
                LocalFilePath=local_file,
                Key=key_name,
            )
        except Exception as e:
            print('err: ' + str(e))
            return -1
        else:
            return 1

    def download_file(self, key_name, dest_file_path):
        try:
            self.client.download_file(
                Bucket=self.bucket_name,
                Key=key_name,
                DestFilePath=dest_file_path,
            )
        except Exception:
            return -1
        else:
            return 1

    def delete_file(self, key_name):
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=key_name,
            )
        except Exception:
            return -1
        else:
            return 1

    def list_file(self, prefix):
        try:
            resp = self.client.list_objects(Bucket=self.bucket_name, Prefix=prefix)
            return resp.get('Contents')[0].get('Key')
        except Exception as e:
            return 'err'


bucket = Bucket(BUCKET_SECRET_ID, BUCKET_SECRET_KEY, BUCKET_NAME, BUCKET_REGION)
