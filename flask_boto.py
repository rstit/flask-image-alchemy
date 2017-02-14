from botocore.config import Config
from flask import current_app

from boto3 import client


class BotoClient:
    app = None

    def __init__(self, service_name, config=None, app=None):
        if app:
            self.init_app(app, service_name, config=config)

    def init_app(self, app, service_name, config=None):
        if not config:
            config = Config(signature_version='s3v4')
        self.ACCESS_KEY = current_app.config.get('AWS_ACCESS_KEY_ID')
        self.SECRET = current_app.config.get('AWS_SECRET_ACCESS_KEY')
        self.REGION_NAME = current_app.config.get('AWS_REGION_NAME')
        self.client = client(
            service_name,
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET,
            region_name=self.REGION_NAME,
            config=config
        )
        self.app = app
