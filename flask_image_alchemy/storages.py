from abc import abstractmethod
from os import makedirs

from os.path import exists, split
from os import remove


class BaseStorage:

    @abstractmethod
    def read(self, file_name): pass

    @abstractmethod
    def write(self, data, file_name): pass

    @abstractmethod
    def delete(self, file_name): pass


class S3Storage(BaseStorage):

    def __init__(self, s3_client, bucket):
        self.s3_client = s3_client
        self.bucket = bucket
        super().__init__()

    def read(self, file_name):
        self.s3_client.download_fileobj(self.bucket, file_name)

    def write(self, data, file_name):
        self.s3_client.upload_fileobj(data, self.bucket, file_name)

    def delete(self, file_name):
        self.s3_client.delete_object(Bucket=self.bucket, Key=file_name)


class FileStorage(BaseStorage):

    def _create_dir_if_needed(self, file_name):
        directory, _ =  split(file_name)
        if directory and not exists(directory):
            makedirs(directory)

    def read(self, file_name):
        with open(file_name, 'r') as file:
            return file.read()

    def write(self, data, file_name):
        self._create_dir_if_needed(file_name)
        with open(file_name, 'wb+') as file:
            file.write(data)

    def delete(self, file_name):
        try:
            remove(file_name)
        except FileNotFoundError:
            pass