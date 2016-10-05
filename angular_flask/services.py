from database import Item as ItemWrapper
from database import Category as CategoryWrapper

class Service:

    model_wrapper = None

    def get(self, id=None):
        if id:
            return self.model_wrapper.get_by_id(id)
        return self.model_wrapper.get_all()

    def post(self, model):
        self.model_wrapper.post(model)

    def patch(self, model):
        self.model_wrapper.patch(model)

    def delete(self, id):
        self.model_wrapper.delete(id)

class ItemService(object, Service):

    model_wrapper = ItemWrapper()

    def get(self, id=None, search=None, category=None):
        if search:
            return self.model_wrapper.search(search)
        elif category:
            return self.model_wrapper.get_by_category(category)
        return super(ItemService, self).get(id=id)

class CategoryService(Service):

    model_wrapper = CategoryWrapper()