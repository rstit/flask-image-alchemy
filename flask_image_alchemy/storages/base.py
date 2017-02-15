from abc import abstractmethod


class BaseStorage:

    @abstractmethod
    def read(self, file_name): pass

    @abstractmethod
    def write(self, data, file_name): pass

    @abstractmethod
    def delete(self, file_name): pass

