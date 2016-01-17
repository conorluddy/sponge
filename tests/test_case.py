import unittest2
from sponge.database import Database
from flask_pymongo import MongoClient
from sponge.utils import load_test_config

class SpongeTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # Attempt to start app instance if it doesn't exist yet
        cls.cfg = load_test_config()

        # DB Connection
        db_client = MongoClient(cls.cfg["database"]["host"], cls.cfg["database"]["port"])
        cls.db = Database(db_client[cls.cfg["database"]["name"]], cls.cfg)

    def assertIsUUID(self, string):
        self.assertIsNotNone(string)
        self.assertEqual(len(string), 36)
        self.assertEqual(string[8], '-')
        self.assertEqual(string[13], '-')
        self.assertEqual(string[18], '-')
        self.assertEqual(string[23], '-')

    @classmethod
    def root(cls):
        return "http://%s:%s" % (cls.cfg["web_server"]["host"], cls.cfg["web_server"]["port"])

    @classmethod
    def req(cls, path, params=None):
        if params:
            return "%s/%s?%s" % (cls.root(), path, params)
        return "%s/%s" % (cls.root(), path)

    #### Fixtures ####

    def new_user(self, **kwargs):
        user = {
            "name": "Joe Bloggs",
            "mail": "jb@mail.com",
            "intro": "hello!",
            "password": "pass"
        }
        for key, value in kwargs.iteritems():
            user[key] = value
        return user

    def new_item(self, **kwargs):
        item = {
            "category": "Clothing",
            "title": "Shoes",
            "description": "Nice Shoes",
            "photos": [],
            "day_rate": 10,
            "week_rate": 40,
            "month_rate": 130,
            "published": True,
            "attributes": {},
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": True,
            "sun": True,
        }
        for key, value in kwargs.iteritems():
            item[key] = value
        return item