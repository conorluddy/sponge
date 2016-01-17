import abc
from document import Document
from sponge.utils import make_uuid

class User(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.mail = kwargs["mail"]
        self.password = kwargs["password"]
        self.intro = kwargs["intro"]
        self.image = kwargs.get("image")
        self.rating = None # Star rating based on user's contract ratings # TODO - update on contract update
        super(User, self).__init__(**kwargs)

    def _json(self):
        return {
            "name": self.name,
            "mail": self.mail,
            "password": self.password, # TODO - encrypt when storing
            "intro": self.intro,
            "image": self.image,
            "rating": self.rating,
        }

    def _uuid(self):
        return make_uuid(str(self.mail))
