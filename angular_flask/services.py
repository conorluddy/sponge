from database import *
from constants import *
from flask import session
from email.utils import parseaddr

class ApiException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class Service(object):

    model_wrapper = None

    def get(self, id=None):
        if id:
            return self.model_wrapper.get_one(id)
        return self.model_wrapper.get_all()

    def post(self, model):
        self.model_wrapper.post(model)

    def patch(self, model):
        self.model_wrapper.patch(model)

    def delete(self, id):
        self.model_wrapper.delete(id)

class SearchService(Service):

    def get(self, id=None, search=None, page=None):
        if search:
            return self.model_wrapper.search(search, page)
        return super(SearchService, self).get(id=id)

class CategoryService(Service):
    model_wrapper = CategoryWrapper()

class CountyService(Service):
    model_wrapper = CountyWrapper()

class ItemService(SearchService):

    model_wrapper = ItemWrapper()

    def get(self, id=None, search=None, page=None, category=None, county=None, lat=None, lng=None):
        if search or category:
            return self.model_wrapper.search(search, page, county, category, lat, lng)
        return super(ItemService, self).get(id=id, search=search, page=page)

class UserService(Service):
    model_wrapper = UserWrapper()

    def get(self):
        return super(UserService, self).get(id=session['user_id'])

    def patch(self, input):
        input['id'] = session['user_id']
        return super(UserService, self).patch(input)

    def register(self, input):
        self._verify_email_available(input['email'])
        self._verify_email_valid(input['email'])
        self._verify_password_valid(input['password'])
        self.model_wrapper.post(input)
        self.login(input)

    def login(self, input):
        self._verify_email_exists(input['email'])
        self._verify_password_match(input['email'], input['password'])
        self._start_session(input['email'])

    def logout(self):
        self._end_session()

    def get_session(self):
        return session

    def _start_session(self, email):
        user = self.model_wrapper.get_one(email, 'email')
        session['user_id'] = user['id']
        session['user_first'] = user['first']
        session['user_last'] = user['last']
        session['email'] = user['email']

    def _end_session(self):
        # TODO - expire sessions
        session.clear()

    def _verify_email_exists(self, email):
        if self.model_wrapper.get_one(email, field='email') is None:
            raise ApiException(EMAIL_NOT_FOUND, status_code=400)

    @staticmethod
    def _verify_password_valid(password):
        if password is None or len(password) < 8:
            raise ApiException(PASSWORD_NOT_VALID, status_code=400)

    @staticmethod
    def _verify_email_valid(email):
        parsed = parseaddr(email) if email else None
        if parsed is None or '@' not in parsed[1] or '.' not in parsed[1]:
            raise ApiException(EMAIL_NOT_VALID, status_code=400)

    def _verify_email_available(self, email):
        if self.model_wrapper.get_one(email, field='email') is not None:
            raise ApiException(EMAIL_ADDRESS_TAKEN, status_code=400)

    def _verify_password_match(self, email, password):
        if not self.model_wrapper.validate_password(email, password):
            raise ApiException(PASSWORD_DOESNT_MATCH, status_code=400)