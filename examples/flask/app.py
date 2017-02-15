import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_image_alchemy.storages import S3Storage
from flask_image_alchemy.fields import StdImageField


db = SQLAlchemy()
s3_storage = S3Storage()


def create_app():
    app = Flask(__name__)

    # SQLAlchemy config
    app.config['SECRET_KEY'] = '123456790'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql+psycopg2://localhost:5432/test'

    # Flask-ImageAlchemy config
    app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID')
    app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    app.config['AWS_REGION_NAME'] = os.environ.get('AWS_REGION_NAME', 'eu-central-1')
    app.config['S3_BUCKET_NAME'] = os.environ.get('AWS_REGION_NAME', 'haraka-local')

    # init extensions
    db.init_app(app)
    s3_storage.init_app(app)

    return app

# create app
app = create_app()


# define main route
@app.route('/')
def index():
    return 'Hello World'


# define models
class ExampleModel(db.Model):
    image = db.Column(
        StdImageField(
            storage=s3_storage,
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        )
    )

def build_db():
    db.drop_all()
    db.create_all()


build_db()
app.run(debug=True)