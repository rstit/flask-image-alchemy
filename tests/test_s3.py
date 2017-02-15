from boto3 import client
from botocore.config import Config

from flask_image_alchemy.storages import S3Storage
from .base import BaseTest
from flask_image_alchemy.fields import StdImageField, StdImageFile
from sqlalchemy import Column, Integer

TEMP_IMAGES_DIR = 'temp_images/'
AMAZON_SERVICE_NAME = 's3'
AWS_ACCESS_KEY = 'xxx'
AWS_SECRET = 'xxx'
AWS_REGION_NAME = 'eu-central-1'
BUCKET_NAME = 'haraka-local'


class TestFieldVariations(BaseTest):

    def setUp(self):
        self.client = client(
            AMAZON_SERVICE_NAME,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET,
            region_name=AWS_REGION_NAME,
            config=Config(signature_version='s3v4')
        )
        super().setUp()

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(
                StdImageField(
                    storage=S3Storage(self.client),
                    variations={"thumbnail": {'height': 100, 'width': 100}}
                ),
                nullable=False
            )
        self.User = User

    def test_create_instance(self):
        u = self.User()
        self.session.add(u)
        self.session.commit()

    def test_upload(self):
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()
            self.assertIsInstance(u.avatar, StdImageFile)
            self.assertIsNotNone(u.avatar.url)
            self.assertIsInstance(u.avatar.thumbnail, StdImageFile)
            self.assertIsNotNone(u.avatar.thumbnail.url)

    def tearDown(self):
        for user in self.session.query(self.User):
            if user.avatar:
                user.avatar.delete(all=True)
        super().tearDown()
