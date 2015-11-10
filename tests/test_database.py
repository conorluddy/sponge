import unittest2
from flask_pymongo import MongoClient
from sponge.database import Database

class TestDatabase(unittest2.TestCase):

    db_name = "sponge"
    db_host = "localhost"
    db_port = 27017
    db_wrapper = None
    db_client = None

    @classmethod
    def setUpClass(cls):
        cls.db_client = MongoClient(cls.db_host, cls.db_port)
        cls.db_wrapper = Database(cls.db_client[cls.db_name])

    @classmethod
    def tearDownClass(cls):
        cls.db_wrapper.remove_all("user")

    def test_add_user(self):
        user_uuid = self.db_wrapper.insert_user(**self._new_user())
        db_user = self.db_wrapper.get_user(user_uuid)

        self.assertEqual(db_user["uuid"], user_uuid)
        self.assertIsNotNone(user_uuid)
        self.assertIsNotNone(db_user)

    def test_remove_user(self):
        user_uuid = self.db_wrapper.insert_user(**self._new_user())
        self.db_wrapper.remove_user(user_uuid)
        db_user = self.db_wrapper.get_user(user_uuid)

        self.assertIsNone(db_user)

    #### Test Data ####

    def _new_user(self):
        return {
            "first": "Joe",
            "last": "Bloggs",
            "mail": "Joe@Bloggs.ie",
            "intro": "Hello",
        }