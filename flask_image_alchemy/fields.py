from tempfile import SpooledTemporaryFile

import sqlalchemy.types as types

from flask_image_alchemy.utils import process_thumbnail, validate_variations, \
    get_unique_filename
from .storages import FileStorage, BaseStorage


class StdImageFile:
    _variations = []

    def __init__(self, storage, json_data):
        self.storage = storage
        self.json_data = json_data
        self._set_attributes()

    def _set_attributes(self):
        setattr(self, "url", self.json_data.pop("original", None))
        for name, url in self.json_data.items():
            setattr(self, name, StdImageFile(self.storage, {"original": url}))
            self._variations.append(url)

    def delete(self, variations=False):
        self.storage.delete(self.url)
        if variations:
            for url in self._variations:
                self.storage.delete(url)


class StdImageField(types.TypeDecorator):

    impl = types.JSON

    def __init__(self, storage:BaseStorage=FileStorage(), variations:dict=None,
                 upload_to=None, media_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.upload_to = upload_to
        self.variations = validate_variations(variations) if variations else None

    def process_bind_param(self, file, dialect):
        if file:
            filename = get_unique_filename(file.filename, self.upload_to)
            # https://github.com/boto/boto3/issues/929
            # https://github.com/matthewwithanm/django-imagekit/issues/391
            temp_file = SpooledTemporaryFile()
            temp_file.write(temp_file.read())
            self.storage.write(temp_file, filename)
            data = {"original": filename}
            if self.variations:
                values = process_thumbnail(file, filename, self.variations, self.storage)
                data.update({key:value for key, value in values})
            return data

    def process_result_value(self, value, dialect):
        if value:
            return StdImageFile(self.storage, value)
