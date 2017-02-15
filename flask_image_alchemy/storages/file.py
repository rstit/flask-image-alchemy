from os import makedirs, remove
from os.path import exists, split

from flask_image_alchemy.storages.base import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self, app=None, media_path=None):
        if app:
            self.init_app(app, media_path)

    def init_app(self, app, media_path):
        self.app = app
        self.media_path = media_path

    def _create_dir_if_needed(self, file_name):
        directory, _ = split(file_name)
        if directory and not exists(directory):
            makedirs(directory)

    def read(self, file_name):
        with open(file_name, 'r') as file:
            return file.read()

    def write(self, file_obj, file_name):
        self._create_dir_if_needed(file_name)
        with open(file_name, 'wb+') as file:
            file.write(file_obj.read())

    def delete(self, file_name):
        try:
            remove(file_name)
        except FileNotFoundError:
            pass
