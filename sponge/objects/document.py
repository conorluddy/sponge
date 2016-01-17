import abc
from uuid import uuid4


class Document():
    __metaclass__ = abc.ABCMeta

    required = []

    def __init__(self, **kwargs):
        self.uuid = self._uuid() if not kwargs.get("uuid") else kwargs["uuid"]

    def to_dict(self):
        self._validate()
        json_document = self._json()
        json_document["uuid"] = self.uuid
        return json_document

    def _validate(self):
        for required_attribute in self.required:
            if not hasattr(self, required_attribute) or getattr(self, required_attribute) is None:
                raise InvalidDocumentException("Doc Type '%s' requires '%s' value" % (self.__class__.__name__,
                                               required_attribute))

    def _uuid(self):
        return str(uuid4())

    @abc.abstractmethod
    def _json(self):
        pass


class InvalidDocumentException(Exception):
    pass
