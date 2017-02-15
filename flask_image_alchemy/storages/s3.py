from boto3 import client
from botocore.config import Config

from flask.ext.image_alchemy.storages.base import BaseStorage


class S3Storage(BaseStorage):

    def __init__(self, app=None, config=None):
        if app:
            self.init_app(app, config=config)

    def init_app(self, app, config=None):
        self.app = app
        self.ACCESS_KEY = app.config.get('AWS_ACCESS_KEY_ID')
        self.SECRET = app.config.get('AWS_SECRET_ACCESS_KEY')
        self.REGION_NAME = app.config.get('AWS_REGION_NAME')
        self.BUCKET_NAME = app.config.get('S3_BUCKET_NAME')
        if not config:
            config = Config(signature_version='s3v4')
        self.client = client(
            's3',
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET,
            region_name=self.REGION_NAME,
            config=config
        )


    def read(self, file_name):
        self.client.download_fileobj(self.BUCKET_NAME, file_name)

    def write(self, data, file_name):
        self.client.upload_fileobj(data, self.BUCKET_NAME, file_name)

    def delete(self, file_name):
        self.client.delete_object(Bucket=self.BUCKET_NAME, Key=file_name)

