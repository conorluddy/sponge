from database import *

class Service(object):

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

class SearchService(Service):

    def get(self, id=None, search=None, page=None):
        if search:
            return self.model_wrapper.search(search, page)
        return super(SearchService, self).get(id=id)

class ItemService(SearchService):

    model_wrapper = ItemWrapper()

    def get(self, id=None, search=None, page=None, category=None, county=None):
        if category:
            return self.model_wrapper.get_by_category(category, page)
        if search:
            return self.model_wrapper.search(search, page, county)
        return super(ItemService, self).get(id=id, search=search, page=page)

class CategoryService(Service):
    model_wrapper = CategoryWrapper()

class CountyService(Service):
    model_wrapper = CountyWrapper()