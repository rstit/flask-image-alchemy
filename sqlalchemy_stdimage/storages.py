from abc import abstractmethod


class BaseStorage:

    @abstractmethod
    def read(self, file_name): pass

    @abstractmethod
    def write(self, data, file_name): pass


class S3Storage(BaseStorage):

    def __init__(self, s3_client):
        self.s3_client = s3_client
        super().__init__()

    def read(self, file_name):
        super().read()

    def write(self, data, file_name):
        super().write()


class FileStorage(BaseStorage):
    def read(self, file_name):
        with open(file_name, 'rb') as file:
            return file.read()

    def write(self, data, file_name):
        with open(file_name, 'wb+') as file:
            file.write(data)