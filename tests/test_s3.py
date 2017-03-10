from unittest.mock import patch

from flask import Flask
from sqlalchemy.event import listen
from werkzeug.datastructures import FileStorage

from flask_image_alchemy.events import before_update_delete_callback, before_delete_delete_callback
from flask_image_alchemy.storages import S3Storage
from .base import BaseTest
from flask_image_alchemy.fields import StdImageField, StdImageFile
from sqlalchemy import Column, Integer

TEMP_IMAGES_DIR = 'tests/temp_images/'
AWS_ACCESS_KEY = 'xxx'
AWS_SECRET = 'xxx'
AWS_REGION_NAME = 'eu-central-1'
BUCKET_NAME = 'test'


class TestS3Storage(BaseTest):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY
        self.app.config['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET
        self.app.config['AWS_REGION_NAME'] = AWS_REGION_NAME
        self.app.config['S3_BUCKET_NAME'] = BUCKET_NAME
        self.s3_storage = S3Storage()
        self.s3_storage.init_app(self.app)
        super().setUp()

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(
                StdImageField(
                    storage=self.s3_storage,
                    variations={"thumbnail": {'height': 100, 'width': 100}}
                ),
                nullable=False
            )
        self.User = User

    @patch('botocore.client.BaseClient._make_api_call')
    def test_create_instance(self, client):
        u = self.User()
        self.session.add(u)
        self.session.commit()

    @patch('botocore.client.BaseClient._make_api_call')
    def test_upload(self, client):
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()
            self.assertIsInstance(u.avatar, StdImageFile)
            self.assertIsNotNone(u.avatar.url)
            self.assertIsNotNone(u.avatar.path)
            self.assertIsInstance(u.avatar.thumbnail, StdImageFile)
            self.assertIsNotNone(u.avatar.thumbnail.url)
            self.assertIsNotNone(u.avatar.thumbnail.path)

    @patch('botocore.client.BaseClient._make_api_call')
    def test_update(self, client):
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()

            _old_avatar_url = u.avatar.url
            _old_avatar_path = u.avatar.path
            _old_thumbnail_url = u.avatar.thumbnail.url
            _old_thumbnail_path = u.avatar.thumbnail.path

            u.avatar = file
            self.session.add(u)
            self.session.commit()

            self.assertIsInstance(u.avatar, StdImageFile)
            self.assertIsNotNone(u.avatar.url)
            self.assertIsNotNone(u.avatar.path)
            self.assertIsInstance(u.avatar.thumbnail, StdImageFile)
            self.assertIsNotNone(u.avatar.thumbnail.url)
            self.assertIsNotNone(u.avatar.thumbnail.path)
            self.assertNotEqual(_old_avatar_url, u.avatar.url)
            self.assertNotEqual(_old_avatar_path, u.avatar.path)
            self.assertNotEqual(_old_thumbnail_url, u.avatar.thumbnail.url)
            self.assertNotEqual(_old_thumbnail_path, u.avatar.thumbnail.path)

            self.assertEqual(client.call_count, 4)  # 4x upload

    @patch('botocore.client.BaseClient._make_api_call')
    def test_update_with_signal(self, client):
        listen(self.User, 'before_update', before_update_delete_callback)
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()

            _old_avatar_url = u.avatar.url
            _old_avatar_path = u.avatar.path
            _old_thumbnail_url = u.avatar.thumbnail.url
            _old_thumbnail_path = u.avatar.thumbnail.path

            u.avatar = file
            self.session.add(u)
            self.session.commit()

            self.assertIsInstance(u.avatar, StdImageFile)
            self.assertIsNotNone(u.avatar.url)
            self.assertIsNotNone(u.avatar.path)
            self.assertIsInstance(u.avatar.thumbnail, StdImageFile)
            self.assertIsNotNone(u.avatar.thumbnail.url)
            self.assertIsNotNone(u.avatar.thumbnail.path)
            self.assertNotEqual(_old_avatar_url, u.avatar.url)
            self.assertNotEqual(_old_avatar_path, u.avatar.path)
            self.assertNotEqual(_old_thumbnail_url, u.avatar.thumbnail.url)
            self.assertNotEqual(_old_thumbnail_path, u.avatar.thumbnail.path)

            self.assertEqual(client.call_count, 6)  # 4x upload, 2x delete

    @patch('botocore.client.BaseClient._make_api_call')
    def test_delete(self, client):
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()

            u.avatar.delete(variations=True)
            u.avatar = None
            self.session.add(u)
            self.session.commit()

            self.assertEqual(client.call_count, 4)  # 2x upload, 2x delete

    @patch('botocore.client.BaseClient._make_api_call')
    def test_delete_with_signal(self, client):
        listen(self.User, 'before_delete', before_delete_delete_callback)
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()

            self.session.delete(u)
            self.session.commit()

            self.assertEqual(client.call_count, 4)  # 2x upload, 2x delete

    @patch('botocore.client.BaseClient._make_api_call')
    def cleanUp(self, client):
        for user in self.session.query(self.User):
            if user.avatar:
                user.avatar.delete(variations=True)

    def tearDown(self):
        self.cleanUp()
        super().tearDown()
