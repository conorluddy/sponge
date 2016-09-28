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

    def get(self, id):
        raise NotImplementedError

    def post(self, model):
        raise NotImplementedError

    def patch(self, model):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

class Item(DatabaseModelWrapper):

    def get(self, id):
        with session_scope() as session:
            item = session.query(ItemModel).filter(ItemModel.id == id).first()
        return item

    def post(self, item):
        with session_scope() as session:
            session.add(item)

    def patch(self, item):
        pass

    def delete(self, id):
        with session_scope() as session:
            session.query(ItemModel).filter(ItemModel.id == id).delete()
