from os import makedirs, remove
from os.path import exists, split

from flask_image_alchemy.storages.base import BaseStorage


class FileStorage(BaseStorage):
    MEDIA_PATH = ''

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.MEDIA_PATH = app.config.get('MEDIA_PATH', '')

    def _create_dir_if_needed(self, file_name):
        directory, _ = split(file_name)
        if directory and not exists(directory):
            makedirs(directory)

    def read(self, file_name):
        with open(self.MEDIA_PATH + file_name, 'r') as file:
            return file.read()

    def write(self, file_obj, file_name):
        full_path = self.MEDIA_PATH + file_name
        self._create_dir_if_needed(full_path)
        with open(full_path, 'wb+') as file:
            file.write(file_obj.read())

    def delete(self, file_name):
        try:
            remove(self.MEDIA_PATH + file_name)
        except FileNotFoundError:
            pass
