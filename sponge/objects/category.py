import abc
from sponge.objects.document import Document
from sponge.utils import make_uuid

class Category(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.image = kwargs["image"]
        self.count = kwargs.get("count")
        super(Category, self).__init__(**kwargs)

    def _json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "image": self.image,
            "count": self.count
        }

    def _uuid(self):
        return make_uuid(self.name)

    def _valid(self):
        return True