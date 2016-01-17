import unittest
import requests
from integration_test_case import SpongeIntegrationTestCase
from sponge.utils import extract_uuid

class TestViews(SpongeIntegrationTestCase):

    def test_index(self):
        self.assertEqual(requests.get(self.root()).status_code, 200)

    #### User ####

    def test_add_user(self):
        resp = requests.post(self.req("user/add"), data=self.new_user(mail="testadd@sponge.ie"))
        user_uuid = extract_uuid(resp.text)

        self.assertEqual(resp.status_code, 200)
        self.assertIsUUID(user_uuid)
        self.assertIsNotNone(self.db.get("user", user_uuid))

    def test_remove_user(self):
        resp = requests.post(self.req("user/add"), data=self.new_user(mail="testremove@sponge.ie"))
        user_uuid = extract_uuid(resp.text)

        self.assertIsNotNone(self.db.get("user", user_uuid))

        resp = requests.get(self.req("user/remove", "uuid=%s" % user_uuid))
        self.assertEqual(resp.status_code, 200)

        self.assertIsNone(self.db.get("user", user_uuid))

    def test_get_user(self):
        resp = requests.post(self.req("user/add"), data=self.new_user(mail="testget@sponge.ie"))
        user_uuid = extract_uuid(resp.text)

        resp = requests.get(self.req("user", "uuid=%s" % user_uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(user_uuid in resp.content)

    def test_replace_user(self):
        resp = requests.post(self.req("user/add"), data=self.new_user(mail="testreplace@sponge.ie"))
        user_uuid = extract_uuid(resp.text)

        resp = requests.get(self.req("user", "uuid=%s" % user_uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(user_uuid in resp.content)

        resp = requests.post(self.req("user/add"),
                             data=self.new_user(uuid=user_uuid, mail="testreplace@sponge.ie", name="replaced_user"))
        self.assertEqual(resp.status_code, 200)

        resp = requests.get(self.req("user", "uuid=%s" % user_uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(user_uuid in resp.content)
        self.assertTrue("replaced" in resp.content)

        self.assertIsNotNone(self.db.get("user", user_uuid))
        self.assertEqual(self.db.get("user", user_uuid)["name"], "replaced_user!")

    #### Items ####

    # def test_add_item(self):
    #     resp = requests.post(self.req("item/add"), data=self.new_user(mail="testadd@sponge.ie"))
    #     print resp.text
    #     user_uuid = extract_uuid(resp.text)
    #
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIsUUID(user_uuid)
    #     self.assertIsNotNone(self.db.get("user", user_uuid))


if __name__ == "__main__":
    unittest.main()
