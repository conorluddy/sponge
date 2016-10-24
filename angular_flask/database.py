from operator import and_
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from angular_flask.core import api_manager
from contextlib import contextmanager
from models import Item, County, Category, User

@contextmanager
def session_scope():
    session = api_manager.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseModelWrapper(object):

    model = None
    page_size = 10

    def get_one(self, value, field="id"):
        with session_scope() as session:
            try:
                return self._map_to_json(session.query(self.model).filter(getattr(self.model, field) == value).one())
            except NoResultFound:
                return None

    def get_all(self):
        with session_scope() as session:
            return self._map_multiple_to_json(session.query(self.model).all())

    def post(self, input):
        with session_scope() as session:
            session.add(self._map_from_json(input))

    def patch(self, input):
        with session_scope() as session:
            db_item = session.query(self.model).filter(self.model.id == input['id']).one()
            for key, value in input.iteritems():
                if not key.startswith("_"):
                    setattr(db_item, key, value)

    def delete(self, id):
        with session_scope() as session:
            session.query(self.model).filter(self.model.id == id).delete()

    def _map_from_json(self, json_input):
        return self.model(**json_input)

    def _map_to_json(self, item):
        return item.to_dict()

    def _map_multiple_to_json(self, items):
        return {"results": [self._map_to_json(item) for item in items]}

class SearchDatabaseModelWrapper(DatabaseModelWrapper):

    def search(self, query, page):
        with session_scope() as session:
            query = session.query(self.model).filter(query)
            query_count = query.count()
            page_query = query.limit(self.page_size).offset(page * self.page_size)
            start = (self.page_size * page) + 1
            end = (start - 1) + self.page_size
            output = self._map_multiple_to_json(page_query.all())
            output.update({
                'page_count': (query_count / self.page_size),
                'page': page,
                'query_count': query.count(),
                'start': start,
                'end': end if end < query_count else query_count
            })
            return output

class ItemWrapper(SearchDatabaseModelWrapper):

    model = Item

    def search(self, searchTerm, page, county, category, lat, lng):
        # TODO - make searching fast, use elasticsearch or something similar
        query = None

        if searchTerm:
            query = or_(
                self.model.description.like('%' + searchTerm + '%'),
                self.model.title.like('%' + searchTerm + '%')
            )

        if category:
            categoryQuery = self.model.category == category
            query = and_(query, categoryQuery) if query else categoryQuery

        if county:
            query = and_(query, self.model.county_id == county)

        return super(ItemWrapper, self).search(query, page)

class CategoryWrapper(DatabaseModelWrapper):
    model = Category

class CountyWrapper(DatabaseModelWrapper):
    model = County

class UserWrapper(DatabaseModelWrapper):
    model = User

    def get_password(self, email):
        # TODO - encrypt stored passwords
        with session_scope() as session:
            return session.query(self.model).filter(self.model.email == email).one().password

    def set_password(self, user_id, password):
        # TODO - encrypt stored passwords
        with session_scope() as session:
            session.query(self.model).filter(self.model.id == user_id).one().password = password
