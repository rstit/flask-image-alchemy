import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from werkzeug.utils import secure_filename
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired

from flask_image_alchemy.storages import S3Storage
from flask_image_alchemy.fields import StdImageField


admin = Admin()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')

    # config
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
    admin.init_app(app)

    return app

# create app
app = create_app()


# define models
class ExampleModel(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(
        StdImageField(
            storage=S3Storage(),
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        ), nullable=True
    )


# define forms
class ExampleModelForm(Form):
    image = FileField('image', validators=[FileRequired()])

# define routes
@app.route('/', methods=('GET', 'POST'))
def index():
    form = ExampleModelForm(csrf_enabled=False)
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
    else:
        filename = None
    return render_template('index.html', form=form, filename=filename)


def build_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


build_db()
app.run(debug=True)