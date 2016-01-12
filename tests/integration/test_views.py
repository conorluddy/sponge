import unittest
from selenium import webdriver
from sponge.utils import extract_uuid

APP_IP = "localhost"
APP_PORT = 5001
WEB_DRIVER = "/Users/ian/Documents/Git/sponge/lib/phantomjs"

class TestViews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_index(self):
        self.driver.get(self._root())
        self.assertIn("Sponge", self.driver.title)

    def test_add_user(self):
        self.driver.get(self._req("user/add", "first=add&last=user&mail=test@add.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._req("user", "uuid=%s" % user_uuid))
        self.assertIsNotNone(user_uuid)
        self.assertTrue(user_uuid in self.driver.page_source)
        self.assertTrue("add" in self.driver.page_source)
        self.assertTrue("user" in self.driver.page_source)

        self.driver.get(self._req("user/remove", "uuid=%s" % user_uuid))

    def test_remove_user(self):
        self.driver.get(self._req("user/add", "first=remove&last=user&mail=test@remove.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._req("user/remove", "uuid=%s" % user_uuid))

        self.driver.get(self._req("user", "uuid=%s" % user_uuid))
        self.assertIsNotNone(user_uuid)
        self.assertFalse(user_uuid in self.driver.page_source)
        self.assertFalse("add" in self.driver.page_source)
        self.assertFalse("user" in self.driver.page_source)

    def test_get_user(self):
        self.driver.get(self._req("user/add", "first=get&last=user&mail=test@get.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._req("user", "uuid=%s" % user_uuid))
        self.assertIsNotNone(user_uuid)
        self.assertTrue(user_uuid in self.driver.page_source)
        self.assertTrue("get" in self.driver.page_source)
        self.assertTrue("user" in self.driver.page_source)

        self.driver.get(self._req("user/remove", "uuid=%s" % user_uuid))

    def test_replace_user(self):
        self.driver.get(self._req("user/add", "first=original&last=user&mail=test@replace.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._req("user/add", "uuid=%s&first=replaced&last=user&mail=test@replace.com&intro=hello&password=password" % user_uuid))

        self.driver.get(self._req("user", "uuid=%s" % user_uuid))
        self.assertIsNotNone(user_uuid)
        self.assertTrue(user_uuid in self.driver.page_source)
        self.assertTrue("replaced" in self.driver.page_source)
        self.assertFalse("original" in self.driver.page_source)

        self.driver.get(self._req("user/remove", "uuid=%s" % user_uuid))

    def _root(self):
        return "http://%s:%s" % (APP_IP, APP_PORT)

    def _req(self, path, params):
        if params:
            return "%s/%s?%s" % (self._root(), path, params)
        return "%s/%s" % (self._root(), path)

if __name__ == "__main__":
    unittest.main()