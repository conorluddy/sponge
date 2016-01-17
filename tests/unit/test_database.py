import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sponge.objects.user import User
from unit_test_case import SpongeUnitTestCase

class TestDatabase(SpongeUnitTestCase):

    def test_add_user(self):
        new_user = self.new_user(mail="testadd@unit.com")

        user_uuid = self.db.insert("user", User(**new_user))

        db_user = self.db.get("user", user_uuid)
        self.assertEqual(db_user["uuid"], user_uuid)
        self.assertIsNotNone(user_uuid)
        self.assertIsNotNone(db_user)

    def test_remove_user(self):
        new_user = self.new_user(mail="testremove@unit.com")
        user_uuid = self.db.insert("user", User(**new_user))

        self.db.remove("user", user_uuid)

        db_user = self.db.get("user", user_uuid)
        self.assertIsNone(db_user)

    def test_replace_user(self):
        new_user = self.new_user(name="newuser", mail="testreplace@unit.com")
        user_uuid = self.db.insert("user", User(**new_user))
        updated_user = self.new_user(name="replaced", mail="testreplace@unit.com")

        self.db.replace("user", user_uuid, User(**updated_user))

        updated_db_user = self.db.get("user", user_uuid)
        self.assertNotEqual(updated_db_user["name"], "newuser")
        self.assertEqual(updated_db_user["name"], "replaced")

    def test_update_user(self):
        new_user = self.new_user(mail="testupdate@unit.com")
        user_uuid = self.db.insert("user", User(**new_user))

        self.db.update("user", user_uuid, {"$set": {"name": "updated"}})

        updated_db_user = self.db.get("user", user_uuid)
        self.assertEqual(updated_db_user["name"], "updated")

    #### Test Data ####

    def _new_user(self, first, last, mail, password, intro):
        return {
            "first": first,
            "last": last,
            "mail": mail,
            "password": password,
            "intro": intro,
        }