from angular_flask.core import db
from angular_flask import app

# TODO - add indexes

class BaseModel:

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def to_dict(self):
        output = self.__dict__
        del output['_sa_instance_state']
        return output

class Item(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    lender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    county = db.relationship('County')
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    def to_dict(self):
        county = self.county.name
        output = super(Item, self).to_dict()
        output['county'] = county
        return output

class County(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class ItemPhoto(db.Model, BaseModel):

    item = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    image = db.Column(db.String, nullable=False)

class Contract(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    borrower = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    cancelled = db.Column(db.Boolean, nullable=False, default=False)
    payment_sent = db.Column(db.Boolean, nullable=False, default=False)
    payment_received = db.Column(db.Boolean, nullable=False, default=False)

class ContractMessage(db.Model, BaseModel):

    stamp = db.Column(db.Integer, nullable=False, primary_key=True)
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    message = db.Column(db.String, nullable=False)

class ContractFeedback(db.Model, BaseModel):

    stamp = db.Column(db.Integer, nullable=False, primary_key=True)
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    message = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Category(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String, nullable=False, default="todo") # TODO

class User(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    photo = db.Column(db.String)
    phone = db.Column(db.String)
    dob = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    phone_verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String, nullable=False) # TODO - encrypt
    intro = db.Column(db.String)

    def to_dict(self):
        output = super(User, self).to_dict()
        del output['password']
        return output