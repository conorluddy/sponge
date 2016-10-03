from angular_flask.core import api_manager
from contextlib import contextmanager
from models import Item as ItemModel

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

    def get(self, id):
        with session_scope() as session:
            item = session.query(self.model).filter(self.model.id == id).one()
        return item

    def post(self, input):
        with session_scope() as session:
            session.add(input)

    def patch(self, input):
        with session_scope() as session:
            db_item = session.query(self.model).filter(self.model.id == input['id']).one()
            for key, value in input.iteritems():
                if not key.startswith("_"):
                    setattr(db_item, key, value)

    def delete(self, id):
        with session_scope() as session:
            session.query(self.model).filter(self.model.id == id).delete()

class Item(DatabaseModelWrapper):

    model = ItemModel