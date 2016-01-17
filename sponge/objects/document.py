import abc
from uuid import uuid4

class Document():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.uuid = self._uuid() if not kwargs.get("uuid") else kwargs["uuid"]

    def to_dict(self):
        if self._valid():
            json_document = self._json()
            json_document["uuid"] = self.uuid
            return json_document
        return None

    def _valid(self):
        return True

    def _uuid(self):
        return str(uuid4())

    @abc.abstractmethod
    def _json(self):
        pass
