from unittest import TestCase
from abc import abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class BaseTest(TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql+psycopg2://localhost:5432/test')
        self.Base = declarative_base()
        Session = sessionmaker(bind=self.engine)
        self.define_models()

        self.session = Session()
        self.Base.metadata.drop_all(self.engine)
        self.Base.metadata.create_all(self.engine)

    @abstractmethod
    def define_models(self): pass

    def tearDown(self):
        self.session.close_all()
        self.Base.metadata.drop_all(self.engine)
        self.engine.dispose()
