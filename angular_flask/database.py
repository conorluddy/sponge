from angular_flask.core import api_manager
from contextlib import contextmanager
from models import Item as ItemModel
from models import Category as CategoryModel

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

class DatabaseModelWrapper:

    model = None

    def get_by_id(self, id):
        with session_scope() as session:
            return self._map_to_json(session.query(self.model).filter(self.model.id == id).one())

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

class Item(DatabaseModelWrapper):

    model = ItemModel

    def search(self, term):
        with session_scope() as session:
            return self._map_multiple_to_json(
                session.query(self.model).filter(self.model.description.like('%' + term + '%')).all())

    def get_by_category(self, categoryId):
        with session_scope() as session:
            return self._map_multiple_to_json(
                session.query(self.model).filter(self.model.category == categoryId).all())

class Category(DatabaseModelWrapper):

    model = CategoryModel
