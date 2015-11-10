import abc
from document import Document

class Item(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.title = kwargs["title"]
        self.description = kwargs["description"]
        self.photos = kwargs["photos"]
        self.user = kwargs["user"]
        self.published = kwargs["published"]
        self.day_rate = kwargs["day_rate"]
        self.mon = kwargs["mon"]
        self.tue = kwargs["tue"]
        self.wed = kwargs["wed"]
        self.thu = kwargs["thu"]
        self.fri = kwargs["fri"]
        self.sat = kwargs["sat"]
        self.sun = kwargs["sun"]
        # TODO - days available, days unavailable

        #### Optional ####

        self.attributes = kwargs.get("attributes")
        self.week_rate = kwargs.get("week_rate")
        self.month_rate = kwargs.get("month_rate")

    def _json(self):
        return {
            "title": self.title,
            "description": self.description,
            "photos": self.photos,
            "user": self.user,
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