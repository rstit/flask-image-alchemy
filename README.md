Flask-ImageAlchemy
===============================
[![Build Status](https://travis-ci.org/rstit/flask-image-alchemy.svg?branch=master)](https://travis-ci.org/rstit/flask-image-alchemy)

version number: 0.0.7

Overview
--------

SQLAlchemy Standarized Image Field for Flask

Features
--------
- Storage backends (FileStorage, S3Storage)
- Thumbnails (wand)
- Flask Application Factory compatible
-

Installation
--------------------

To install use pip:
```bash
$ pip install Flask-ImageAlchemy
```

Or clone the repo:
```bash
$ git clone https://github.com/rstit/flask-image-alchemy.git
$ python setup.py install
```
Usage
-----
#### SQLAlchemy Model
```python
storage = S3Storage()
storage.init_app(app)

class User(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(
        StdImageField(
            storage=storage,
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        ), nullable=True
    )
```
#### Flask Settings
If you need S3Starage, set up config in your flask application:
```python
AWS_ACCESS_KEY_ID = "you-api-key"
AWS_SECRET_ACCESS_KEY = "you-secret-key"
AWS_REGION_NAME = "bucket-region"
S3_BUCKET_NAME = "bucket-name"
```

If you need FileStorage and custom `MEDIA_PATH`:
```python
MEDIA_PATH = "/var/www/assets/images/"
```
#### Usage in views
```python
u = User()
u.avatar = file # werkzeug.datastructures.FileStorage
u.save()
```
And you have access to thumbnails:
```python
u.avatar.url
u.avatar.thumbnail
u.avatar.thumbnail.url
u.avatar.thumbnail.path
```
#### Deleting images

Django dropped support for automated deletions in version 1.3. Implementing file deletion should 
be done inside your own applications using the `before_delete` signal. Clearing the field if blank is 
true, does not delete the file. This can also be achieved using `before_update` signals. This 
packages contains two event callback methods that handle file deletion for all SdtImageFields of a 
model.

```python
from flask_image_alchemy.events import before_update_delete_callback, before_delete_delete_callback
from sqlalchemy.event import listen
listen(User, 'before_update', before_update_delete_callback)
listen(User, 'before_delete', before_delete_delete_callback)
```

TODO
------------
* Validators (MinSizeValidator, MaxSizeValidator)
* Flask-Admin widget
* Coverage
* Docs Page
* Async Jobs (Image Processing)