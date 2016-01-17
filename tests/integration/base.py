import requests
import unittest
from sponge.database import Database
from time import sleep
import sys
import os
from flask_pymongo import MongoClient
from sponge.utils import read_json_file

WEB_DRIVER = "/Users/ian/Documents/Git/sponge/lib/phantomjs"
CONFIG = "/Users/ian/Documents/Git/sponge/test.json"

class SpongeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Attempt to start app instance if it doesn't exist yet
        cls.cfg = read_json_file(CONFIG)

        # DB Connection
        db_client = MongoClient(cls.cfg["database"]["host"], cls.cfg["database"]["port"])
        cls.db = Database(db_client[cls.cfg["database"]["name"]], cls.cfg)

        # Start App if not running
        cls._start_app()
        cls._wait_for_app()

    @classmethod
    def tearDownClass(cls):
        # Kill app
        cls._stop_app()

    @classmethod
    def _start_app(cls):
        if not cls._ping_app():
            os.popen(cls.cfg["executable"])

    @classmethod
    def _wait_for_app(cls):
        sleep(2)
        timeout = 5
        while timeout > 0 and not cls._ping_app():
            sleep(1)
            timeout -= 1
        if timeout == 0:
            sys.exit('App not running!')

    @classmethod
    def _ping_app(cls):
        try:
            return requests.get(cls.req('')).status_code == 200
        except Exception as ex:
            print str(ex)
            return False

    @classmethod
    def _stop_app(cls):
        os.popen("kill $(ps aux | grep 'test.json' | awk '{print $2}')")

    #### Utils ####

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

    # def new_item(self, **kwargs):
    #     item = {
    #         "category": "Clothing",
    #         "title": "Shoes",
    #         "description": "Nice Shoes",
    #         "photos": [],
    #         "lender": "86220d1c-787f-5872-96f8-4194b4887984"
    #     }
    #
    #     self.category = kwargs["category"]
    #     self.title = kwargs["title"]
    #     self.description = kwargs["description"]
    #     self.photos = kwargs["photos"]
    #     self.lender = kwargs["lender"]
    #     self.day_rate = kwargs["day_rate"]
    #     self.mon = kwargs["mon"]
    #     self.tue = kwargs["tue"]
    #     self.wed = kwargs["wed"]
    #     self.thu = kwargs["thu"]
    #     self.fri = kwargs["fri"]
    #     self.sat = kwargs["sat"]
    #     self.sun = kwargs["sun"]
    #     # TODO - days available, days unavailable
    #
    #     self.attributes = kwargs.get("attributes")
    #     self.published = kwargs.get("published", False)
    #     self.week_rate = kwargs.get("week_rate")
    #     self.month_rate = kwargs.get("month_rate")