import abc
from document import Document

class Item(Document):
    __metaclass__ = abc.ABCMeta

    required = ['category', 'title', 'description', 'lender']

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.category = kwargs.get("category")
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.photos = kwargs.get("photos")
        self.lender = kwargs.get("lender")
        self.day_rate = kwargs.get("day_rate")
        self.mon = kwargs.get('mon', True)
        self.tue = kwargs.get('tue', True)
        self.wed = kwargs.get('wed', True)
        self.thu = kwargs.get('thu', True)
        self.fri = kwargs.get('fri', True)
        self.sat = kwargs.get('sat', True)
        self.sun = kwargs.get('sun', True)
        self.attributes = kwargs.get("attributes")
        self.published = kwargs.get("published", False)
        self.week_rate = kwargs.get("week_rate")
        self.month_rate = kwargs.get("month_rate")

    def _json(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "photos": self.photos,
            "lender": self.lender,
            "published": self.published,
            "day_rate": self.day_rate,
            "week_rate": self.week_rate,
            "month_rate": self.month_rate,
            "mon": self.mon,
            "tue": self.tue,
            "wed": self.wed,
            "thu": self.thu,
            "fri": self.fri,
            "sat": self.sat,
            "sun": self.sun,
            "attributes": self.attributes
        }
