import unittest
from selenium import webdriver
from sponge.utils import extract_uuid

APP_IP = "localhost"
APP_PORT = 5000
# WEB_DRIVER = "C:\\chromedriver.exe"
WEB_DRIVER = "C:\\phantomjs.exe"

class TestViews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.driver = webdriver.Chrome(WEB_DRIVER, service_args=['--ignore-ssl-errors=true'])
        cls.driver = webdriver.PhantomJS(WEB_DRIVER, service_args=['--ignore-ssl-errors=true'])

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_index(self):
        self.driver.get(self._root())
        self.assertIn("Sponge", self.driver.title)

    def test_add_user(self):
        self.driver.get(self._post("user/add", "first=add&last=user&mail=test@aol.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._post("user", "uuid=%s" % user_uuid))
        self.assertTrue(user_uuid in self.driver.page_source)
        self.assertTrue("add" in self.driver.page_source)
        self.assertTrue("user" in self.driver.page_source)

    def test_remove_user(self):
        self.driver.get(self._post("user/add", "first=remove&last=user&mail=test@aol.com&intro=hello&password=password"))
        user_uuid = extract_uuid(self.driver.page_source)

        self.driver.get(self._post("user/remove", "uuid=%s" % user_uuid))

        self.driver.get(self._post("user", "uuid=%s" % user_uuid))
        self.assertFalse(user_uuid in self.driver.page_source)
        self.assertFalse("add" in self.driver.page_source)
        self.assertFalse("user" in self.driver.page_source)

    def _root(self):
        return "http://%s:%s" % (APP_IP, APP_PORT)

    def _get(self, path):
        return "%s/%s" % (self._root(), path)

    def _post(self, path, params):
        return "%s/%s?%s" % (self._root(), path, params)

if __name__ == "__main__":
    unittest.main()