SQLAlchemy-Utils
================

|Build Status| |Version Status|


Various utility functions, new data types and helpers for SQLAlchemy.

Features
--------
- Storage backends (FileStorage, S3Storage)
- Thumbnails (wand)
- Image Validators (MaxSizeValidator, MinSizeValidator)
- Async Jobs (Celery)
- Flask Admin widget
- Flask Application Factory compatible

Examples
--------
```python
from sqlalchemy_stdimage.storages import S3Storage

from app.extensions import boto
from sqlalchemy_stdimage.fields import StdImageField


class ExampleModel:
    image = StdImageField(storage=S3Storage(boto.client), variations={
        'thumbnail': {"width": 100, "height": 100, "crop": True}
    })
```

BotoExtension
```python
from flask_boto import BotoClient

boto = BotoClient('s3')
```

FlaskAdmin
```python
from sqlalchemy_stdimage.admin import StdImageField


class ExampleAdmin(ModelView):
    form_overrides = {
        'image': StdImageField
    }
```

Resources
---------

- `Documentation <https://sqlalchemy-stdimage.readthedocs.io/>`_
- `Issue Tracker <http://github.com/rstit/sqlalchemy-stdimage/issues>`_
- `Code <http://github.com/rstit/sqlalchemy-stdimage/>`_

.. |Build Status| image:: https://travis-ci.org/rstit/sqlalchemy-stdimage.svg?branch=master
   :target: https://travis-ci.org/rstit/sqlalchemy-stdimage
.. |Version Status| image:: https://img.shields.io/pypi/v/SQLAlchemy-StdImage.svg
   :target: https://pypi.python.org/pypi/SQLAlchemy-StdImage/
