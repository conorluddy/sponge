from database import Item as ItemWrapper
from models import Item as ItemModel

class Service:

    model_wrapper = None

    def _map(self, input):
        raise NotImplementedError

    def _unmap(self, model):
        raise NotImplementedError

    def get(self, id):
        return self._unmap(self.model_wrapper.get(id))

    def post(self, model):
        self.model_wrapper.post(self._map(model))

    def patch(self, model):
        self.model_wrapper.patch(model)

    def delete(self, id):
        self.model_wrapper.delete(id)

class ItemService(Service):

    model_wrapper = ItemWrapper()

    def _map(self, json_input):
        return ItemModel(**json_input)

    def _unmap(self, model):
        return model.__dict__




