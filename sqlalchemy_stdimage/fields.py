import sqlalchemy.types as types
from .storages import FileStorage

class StdImageField(types.TypeDecorator):

    impl = types.JSON

    def __init__(self, storage=FileStorage(), variations=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.variations = variations

    def process_bind_param(self, file, dialect):
        if file:
            self.storage.write(file.read(), "temp"+file.name.split("/")[1])
            return {
                "original": file.name
            }

    def process_result_value(self, value, dialect):
        return value.get("original")
