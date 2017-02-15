import sqlalchemy.types as types

from sqlalchemy_stdimage.utils import process_thumbnail, validate_variations, \
    get_unique_filename
from .storages import FileStorage, BaseStorage


class StdImageFile:
    def __init__(self, storage, json_data):
        self.storage = storage
        self.json_data = json_data
        self._set_attributes()

    def _set_attributes(self):
        setattr(self, "url", self.json_data.pop("original", None))
        for name, url in self.json_data.items():
            setattr(self, name, StdImageFile(self.storage, {"original": url}))

    def delete(self, all=False):
        self.storage.delete(self.url)

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
            filename = get_unique_filename(file.name, self.upload_to)
            self.storage.write(file.read(), filename)
            data = {"original": filename}
            if self.variations:
                values = process_thumbnail(file, filename, self.variations, self.storage)
                data.update({key:value for key, value in values})
            return data

    def process_result_value(self, value, dialect):
        if value:
            return StdImageFile(self.storage, value)
