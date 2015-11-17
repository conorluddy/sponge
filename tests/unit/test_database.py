import unittest2
from flask_pymongo import MongoClient
from sponge.database import Database
from sponge.objects.user import User

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
        cls.db_wrapper.remove_all("category")

    def test_add_user(self):
        new_user = self._new_user("Test", "Add", "test@add.db", "intro")

        user_uuid = self.db_wrapper.insert("user", User(**new_user))

        db_user = self.db_wrapper.get("user", user_uuid)
        self.assertEqual(db_user["uuid"], user_uuid)
        self.assertIsNotNone(user_uuid)
        self.assertIsNotNone(db_user)

    def test_remove_user(self):
        new_user = self._new_user("Test", "Remove", "test@remove.db", "intro")
        user_uuid = self.db_wrapper.insert("user", User(**new_user))

        self.db_wrapper.remove("user", user_uuid)

        db_user = self.db_wrapper.get("user", user_uuid)
        self.assertIsNone(db_user)

    def test_replace_user(self):
        new_user = self._new_user("Test", "Replace", "test@replace.db", "intro")
        user_uuid = self.db_wrapper.insert("user", User(**new_user))
        updated_user = self._new_user("User", "Replaced", "test@replace.db", "intro")

        self.db_wrapper.replace("user", user_uuid, User(**updated_user))

        updated_db_user = self.db_wrapper.get("user", user_uuid)
        self.assertNotEqual(updated_db_user["first"], new_user["first"])
        self.assertNotEqual(updated_db_user["last"], new_user["last"])

    def test_update_user(self):
        new_user = self._new_user("Test", "Update", "test@update.db", "intro")
        user_uuid = self.db_wrapper.insert("user", User(**new_user))

        self.db_wrapper.update("user", user_uuid, {"$set": {"first": "Updated", "last": "User"}})

        updated_db_user = self.db_wrapper.get("user", user_uuid)
        self.assertEqual(updated_db_user["first"], "Updated")
        self.assertEqual(updated_db_user["last"], "User")

    #### Test Data ####

    def _new_user(self, first, last, mail, intro):
        return {
            "first": first,
            "last": last,
            "mail": mail,
            "intro": intro,
        }