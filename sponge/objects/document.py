import abc

class Document():
    __metaclass__ = abc.ABCMeta

    def to_dict(self):
        if self._valid():
            return self._json()
        return None

    @abc.abstractmethod
    def _valid(self):
        pass

    @abc.abstractmethod
    def _json(self):
        pass