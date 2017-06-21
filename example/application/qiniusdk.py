# -*- coding:utf8 -*-

from application import app
from qiniu import Auth, put_stream, put_file, etag, urlsafe_base64_encode
import os

access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
bucket_name = app.config['QINIU_BUCKET_NAME']

q = Auth(access_key, secret_key)

def save_file_to_cloud(save_filename, source_file):
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_filename)
    save_dir = os.path.join(os.getcwd(), app.config['UPLOAD_DIR'])
    # filepath = os.path.join(save_dir, save_filename)
    filepath = os.path.join(save_dir, 'temp')
    source_file.save(filepath)
    ret, info = put_file(token, save_filename, filepath)

    # ret, info = put_stream(token, save_filename, source_file.stream,
    #                        "qiniu" ,os.fstat(source_file.stream.fileno()).st_size)
    print info
    if info.status_code == 200:
        return os.path.join(app.config['QINIU_DOMAIN'], save_filename)
    return None

