import json
import logging

from utils import strip_dict

class Database():
    """
    Wrapper for the database layer
    """
    PAGE_SIZE = 15

    def __init__(self, db):
        self.db = db
        self.create_indexes()

    def create_indexes(self):
        self.db.user.create_index("id")

    def reset_database(self):
        self.db.user.drop()

    def insert_user(self, user):
        self.insert_document(self.db.user, user)

    def get_user(self, id):
        return self.query("user", {"id": id})

    def insert_document(self, collection_name, document):
        json_document = document.to_dict()
        if json_document:
            logging.info("Ins: col=%s doc=%s" % (collection_name, json_document))
            self._get_collection(collection_name).insert(json_document)

    def remove(self, collection_name, query):
        logging.info("Rem: col=%s qry=%s" % (collection_name, query))

        self._get_collection(collection_name).remove(strip_dict(query))

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
        return self._get_collection(collection_name).find_one(sort=[(key, -1)])[key]

    def min(self, collection_name, key):
        return self._get_collection(collection_name).find_one(sort=[(key, 1)])[key]

    #### Internal ####

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
    def _serialise_document(object):
        del object["_id"] # Delete unserialisable mongo id
        return object

    def _serialise(self, cursor):
        return [self._serialise_document(obj) for obj in cursor]

    def _get_collection(self, collection_name):
        return getattr(self.db, collection_name)