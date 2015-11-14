import abc
from utils import random_uuid

class Document():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.uuid = self._uuid() if not "uuid" in kwargs else kwargs["uuid"]

    def to_dict(self):
        if self._valid():
            json_document = self._json()
            json_document["uuid"] = self.uuid
            return json_document
        return None

    @abc.abstractmethod
    def _valid(self):
        pass

    @abc.abstractmethod
    def _json(self):
        pass

    @abc.abstractmethod
    def _uuid(self):
        pass