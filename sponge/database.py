import json
import logging

from utils import strip_dict, make_uuid
from constants import CATEGORIES
from objects.category import Category
from objects.item import Item
from objects.user import User

class Database():
    """
    Wrapper for the database layer
    """
    PAGE_SIZE = 15

    def __init__(self, db):
        self.db = db
        self.create_indexes()
        self.create_defaults()

    def create_indexes(self):
        self.db.user.create_index("uuid")
        self.db.item.create_index("uuid")
        self.db.category.create_index("uuid")

    def create_defaults(self):

        # Insert categories
        for name, image in CATEGORIES:
            if not self.get("category", make_uuid(name)):
                self.insert("category", Category(name=name, image=image))

    def reset_database(self):
        self.db.user.drop()
        self.db.item.drop()
        self.db.category.drop()

    def insert_or_replace(self, collection_name, uuid, document):
        if uuid:
            return self.replace(collection_name, uuid, document)
        return self.insert(collection_name, document)

    def insert(self, collection_name, document):
        json_document = document.to_dict()
        if json_document:
            logging.info("Ins: col=%s doc=%s" % (collection_name, json_document))
            self._get_collection(collection_name).insert(json_document)
            return json_document["uuid"]
        return None

    def update(self, collection_name, document_uuid, update_dict):
        logging.info("Upd: col=%s uuid=%s upd=%s" % (collection_name, document_uuid, update_dict))
        self._get_collection(collection_name).update({'uuid': document_uuid}, update_dict)
        return document_uuid

    def replace(self, collection_name, document_uuid, document):
        json_document = document.to_dict()
        json_document["uuid"] = document_uuid
        logging.info("Rpl: col=%s uuid=%s doc=%s" % (collection_name, document_uuid, json_document))
        self._get_collection(collection_name).update({'uuid': document_uuid}, json_document)
        return document_uuid

    def remove(self, collection_name, document_uuid):
        logging.info("Rem: col=%s qry=%s" % (collection_name, {"uuid": document_uuid}))
        self._get_collection(collection_name).remove({"uuid": document_uuid})

    def remove_all(self, collection_name):
        logging.info("RemAll: col=%s " % collection_name)
        self._get_collection(collection_name).remove({})

    def get(self, collection_name, document_uuid):
        return self._serialise_document(self._get_collection(collection_name).find_one({"uuid": document_uuid}))

    def query(self, collection_name, query, sort_by=None, sort_dir=None, page=None):
        logging.info("Qry: col=%s qry=%s srt=%s:%s pg=%s" % (collection_name, query, sort_by, sort_dir, page ) )

        result = self._get_collection(collection_name).find(strip_dict(query))
        count = result.count()

        # Sorting
        if sort_by is not None:
            sort_dir = 1 if sort_dir is None else int(sort_dir) # 1 = ascending, -1 = descending
            result = result.sort(sort_by, sort_dir)

        # Pagination
        if page is not None:
            result = result.limit(self.PAGE_SIZE).skip(int(page) * self.PAGE_SIZE)

        return self._serialise(result), count

    def all(self, collection_name):
        return self._serialise(self._get_collection(collection_name).find())

    def count(self, collection_name):
        return self._get_collection(collection_name).find().count()

    def distinct(self, collection_name, key):
        return self._get_collection(collection_name).find().distinct(key)

    def range(self, collection_name, key):
        return {
            "max": self.max(collection_name, key),
            "min": self.min(collection_name, key),
        }

    def max(self, collection_name, key):
        return self._get_collection(collection_name).get(sort=[(key, -1)])[key]

    def min(self, collection_name, key):
        return self._get_collection(collection_name).get(sort=[(key, 1)])[key]

    @staticmethod
    def _all(arguments):
        if arguments not in [None, []]:
            return {"$all": json.loads(arguments)}

    @staticmethod
    def _gt(arguments):
        if arguments not in [None, []]:
            return {"$gt": arguments}

    @staticmethod
    def _lt(arguments):
        if arguments not in [None, []]:
            return {"$lt": arguments}

    @staticmethod
    def _in(arguments):
        if arguments is not None:
            if not arguments:
                return {"$in": arguments}
            return {"$in": json.loads(arguments)}

    @staticmethod
    def _in_range(arguments):
        if arguments is not None:
            range = json.loads(arguments)
            return {"$gte": range[0], "$lte": range[1]}

    @staticmethod
    def _serialise_document(db_object):
        if db_object:
            del db_object["_id"] # Delete unserialisable mongo id
            return db_object

    def _serialise(self, cursor):
        return [self._serialise_document(obj) for obj in cursor]

    def _get_collection(self, collection_name):
        return getattr(self.db, collection_name)

    #### User ####

    def insert_user(self, **kwargs):
        # TODO - validate
        return self.insert_or_replace("user", kwargs.get("uuid"), User(**kwargs))

    def remove_user(self, user_id):
        # TODO - validate
        return self.remove("user", user_id)

    def get_user(self, user_id):
        return self.get("user", user_id)

    #### Item ####

    def insert_item(self, **kwargs):
        return self.insert_or_replace("item", kwargs.get("uuid"), Item(**kwargs))

    def remove_item(self, item_uuid):
        return self.remove("item", item_uuid)

    def get_item(self, item_uuid):
        return self.get("item", item_uuid)