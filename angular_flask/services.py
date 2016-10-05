from database import Item as ItemWrapper
from database import Category as CategoryWrapper

class Service:

    model_wrapper = None

    def get(self, id=None, search=None):
        if search is not None:
            return self.model_wrapper.search(search)
        elif id is not None:
            return self.model_wrapper.get_with_id(id)
        else:
            return self.model_wrapper.get_all()

    def post(self, model):
        self.model_wrapper.post(model)

    def patch(self, model):
        self.model_wrapper.patch(model)

    def delete(self, id):
        self.model_wrapper.delete(id)

class ItemService(Service):

    model_wrapper = ItemWrapper()

class CategoryService(Service):

    model_wrapper = CategoryWrapper()