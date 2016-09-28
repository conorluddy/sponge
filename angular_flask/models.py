from datetime import datetime

from angular_flask.core import db
from angular_flask import app

# TODO - use UUIDS
# TODO - add indexes

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    lender = db.Column(db.Integer, nullable=False)
    day_rate = db.Column(db.Float, nullable=False)
    published = db.Column(db.Boolean, default=False, nullable=False)
    week_rate = db.Column(db.Float)
    month_rate = db.Column(db.Float)
    mon = db.Column(db.Boolean, default=True, nullable=False)
    tue = db.Column(db.Boolean, default=True, nullable=False)
    wed = db.Column(db.Boolean, default=True, nullable=False)
    thu = db.Column(db.Boolean, default=True, nullable=False)
    fri = db.Column(db.Boolean, default=True, nullable=False)
    sat = db.Column(db.Boolean, default=True, nullable=False)
    sun = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.category = kwargs["category"]
        self.title = kwargs["title"]
        self.description = kwargs["description"]
        self.lender = kwargs["lender"]
        self.day_rate = kwargs["day_rate"]

        self.week_rate = kwargs.get("week_rate")
        self.month_rate = kwargs.get("month_rate")
        self.published = kwargs.get("published")
        self.mon = kwargs.get("mon")
        self.tue = kwargs.get("tue")
        self.wed = kwargs.get("wed")
        self.thu = kwargs.get("thu")
        self.fri = kwargs.get("fri")
        self.sat = kwargs.get("sat")
        self.sun = kwargs.get("sun")

class Contract(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, nullable=False)
    borrower = db.Column(db.Integer, nullable=False)
    lender = db.Column(db.Integer, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    cancelled = db.Column(db.Boolean, nullable=False, default=False)
    payment_sent = db.Column(db.Boolean, nullable=False, default=False)
    payment_received = db.Column(db.Boolean, nullable=False, default=False)
    conversation = db.Column(db.String)

    def __init__(self, **kwargs):
        self.item = kwargs["item"]
        self.borrower = kwargs["borrower"]
        self.lender = kwargs["lender"]
        self.start_date = kwargs["start_date"]
        self.end_date = kwargs["end_date"]
        self.cost = kwargs["cost"]
        super(Contract, self).__init__(**kwargs)

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80)) # TODO - encrypt
    intro = db.Column(db.Text, nullable=True)

    def __init__(self, **kwargs):
        self.first = kwargs["first"]
        self.last = kwargs["last"]
        self.email = kwargs["email"]
        self.password = kwargs["password"]

        self.intro = kwargs.get("intro")

# models for which we want to create API endpoints
app.config['API_MODELS'] = {
    'item': Item,
    'user': User,
    'category': Category,
    'contract': Contract,
}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {
    'item': Item,
    'user': User,
    'contract': Contract,
}
