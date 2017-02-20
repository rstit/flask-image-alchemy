Flask-ImageAlchemy
===============================
[![Build Status](https://travis-ci.org/rstit/flask-image-alchemy.svg?branch=master)](https://travis-ci.org/rstit/flask-image-alchemy)

version number: 0.0.4

Overview
--------

SQLAlchemy Standarized Image Field for Flask

Features
--------
- Storage backends (FileStorage, S3Storage)
- Thumbnails (wand)
- Flask Application Factory compatible

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
Create model with StdImageField
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
If you need S3Starage, set up config in your flask application:
```python
AWS_ACCESS_KEY_ID = "you-api-key"
AWS_SECRET_ACCESS_KEY = "you-secret-key"
AWS_REGION_NAME = "bucket-region"
S3_BUCKET_NAME = "bucket-name"
```


If you need filestorage with different MEDIA_PATH
```python
MEDIA_PATH = "/var/www/assets/images/"
```

Then you can use image field
```python
u = User()
u.avatar = file
u.save()
```
And you have access to thumbnails:
```python
u.avatar.url
u.avatar.thumbnail
u.avatar.thumbnail.url
u.avatar.thumbnail.path
```


TODO
------------
* Validators (MinSizeValidator, MaxSizeValidator)
* Flask-Admin widget
* Coverage
* Docs Page
* Async Jobs (Image Processing)