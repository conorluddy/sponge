import abc
from sponge.objects.document import Document

class User(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.mail = kwargs["mail"]
        self.intro = kwargs["intro"]
        self.image = kwargs.get("image")
        self.rating = None

    def _valid(self):
        return True

    def _json(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
            "intro": self.intro,
            "image": self.image,
            "rating": self.rating,
        }