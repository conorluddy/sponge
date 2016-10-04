from database import Item as ItemWrapper
from database import Category as CategoryWrapper

class Service:

    model_wrapper = None

    def get(self, id):
        return self.model_wrapper.get(id)

    def get_all(self):
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