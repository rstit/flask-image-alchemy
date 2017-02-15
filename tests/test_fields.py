from .base import BaseTest
from sqlalchemy_stdimage.fields import StdImageField
from sqlalchemy import Column, Integer

TEMP_IMAGES_DIR = 'temp_images/'

class TestField(BaseTest):

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(StdImageField(), nullable=False)
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


class TestFieldVariations(BaseTest):

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(
                StdImageField(
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
            x = u.avatar