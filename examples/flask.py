from flask_image_alchemy.storages import S3Storage

from flask_image_alchemy.fields import StdImageField


class ExampleModel:
    image = StdImageField(
        storage=S3Storage(boto.client),
        variations={
            'thumbnail': {"width": 100, "height": 100, "crop": True}
        }
    )