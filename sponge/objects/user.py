import abc
from document import Document

class User(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.first = kwargs["first"]
        self.last = kwargs["last"]
        self.mail = kwargs["mail"]
        self.intro = kwargs["intro"]
        self.image = kwargs.get("image")
        self.rating = None

    def _valid(self):
        return True

    def _json(self):
        return {
            "first": self.first,
            "last": self.last,
            "mail": self.mail,
            "intro": self.intro,
            "image": self.image,
            "rating": self.rating,
        }