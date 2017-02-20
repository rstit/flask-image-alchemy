from boto3 import client
from botocore.config import Config

from flask_image_alchemy.storages.base import BaseStorage
# Find the stack on which we want to store s3 client.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class S3Storage(BaseStorage):

    def __init__(self, app=None, config=None):
        if app:
            self.init_app(app, config=config)

    def _create_client(self):
        return client(
            's3',
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET,
            region_name=self.REGION_NAME,
            config=self.config
        )

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 's3_service'):
                ctx.s3_service = self._create_client()
            return ctx.s3_service
        else:
            # If you want to use s3 client outside flask application
            return self._create_client()

    def init_app(self, app, config=None):
        self.app = app
        self.ACCESS_KEY = app.config.get('AWS_ACCESS_KEY_ID')
        self.SECRET = app.config.get('AWS_SECRET_ACCESS_KEY')
        self.REGION_NAME = app.config.get('AWS_REGION_NAME')
        self.BUCKET_NAME = app.config.get('S3_BUCKET_NAME')
        self.config = config if config else Config(signature_version='s3v4')

    def read(self, file_name):
        self.client.download_fileobj(self.BUCKET_NAME, file_name)

    def write(self, data, file_name):
        self.client.upload_fileobj(data, self.BUCKET_NAME, file_name)

    def delete(self, file_name):
        self.client.delete_object(Bucket=self.BUCKET_NAME, Key=file_name)

