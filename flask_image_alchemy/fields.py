from tempfile import TemporaryFile

import sqlalchemy.types as types

from flask_image_alchemy.utils import process_thumbnail, validate_variations, \
    get_unique_filename
from .storages import FileStorage, BaseStorage


class StdImageFile:
    _variations = []

    def __init__(self, storage, json_data):
        self._variations.clear()
        self.storage = storage
        self.json_data = json_data
        self._set_attributes()

    def _build_full_url(self, path):
        if isinstance(self.storage, FileStorage):
            url = "{media_path}{path}"
            return url.format(
                media_path=self.storage.MEDIA_PATH,
                path=path
            )
        else:
            url = "https://{bucket_name}.s3-{region_name}.amazonaws.com/{path}"
            return url.format(
                region_name=self.storage.REGION_NAME,
                bucket_name=self.storage.BUCKET_NAME,
                path=path
            )

    def _set_attributes(self):
        original_path = self.json_data.pop("original", None)
        full_url = self._build_full_url(original_path)
        setattr(self, "url", full_url)
        setattr(self, "path", original_path)
        for name, url in self.json_data.items():
            setattr(self, name, StdImageFile(self.storage, {"original": url}))
            self._variations.append(url)

    def delete(self, variations=False):
        self.storage.delete(self.path)
        if variations:
            for path in self._variations:
                self.storage.delete(path)


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
            temp_file = TemporaryFile()
            temp_file.write(file.read())
            temp_file.seek(0)
            self.storage.write(temp_file, filename)
            data = {"original": filename}
            if self.variations:
                values = process_thumbnail(file, filename, self.variations, self.storage)
                data.update({key:value for key, value in values})
            return data

    def process_result_value(self, value, dialect):
        if value:
            return StdImageFile(self.storage, value)
