from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from werkzeug.utils import secure_filename
from flask_wtf import Form
from flask_wtf.file import FileField

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

    # init extensions
    admin.init_app(app)
    db.init_app(app)

    return app

# create app
app = create_app()


# define models
class ExampleModel(db.Model):
    image = db.Column(
        StdImageField(
            storage=S3Storage(),
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        )
    )


# define forms
class ExampleModelForm(Form):
    image = FileField('Your photo')

# define routes
@app.route('/', methods=('GET', 'POST'))
def index():
    form = ExampleModelForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
    else:
        filename = None
    return render_template('upload.html', form=form, filename=filename)


def build_db():
    db.drop_all()
    db.create_all()


build_db()
app.run(debug=True)