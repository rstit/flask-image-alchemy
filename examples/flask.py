from sqlalchemy_stdimage.storages import S3Storage

from sqlalchemy_stdimage.fields import StdImageField


class ExampleModel:
    image = StdImageField(
        storage=S3Storage(boto.client),
        variations={
            'thumbnail': {"width": 100, "height": 100, "crop": True}
        }
    )