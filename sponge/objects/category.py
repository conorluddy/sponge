import abc
from sponge.objects.document import Document

class Category(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        self.name = kwargs["name"]
        self.image = kwargs["image"]
        self.count = kwargs.get("count")

    def _json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "image": self.image,
            "count": self.count
        }