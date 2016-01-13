import requests
import unittest
import json
from time import sleep
import sys
import os
from selenium import webdriver
from sponge.utils import read_config_file

WEB_DRIVER = "/Users/ian/Documents/Git/sponge/lib/phantomjs"
CONFIG = "/Users/ian/Documents/Git/sponge/test.json"

class SpongeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Attempt to start app instance if it doesn't exist yet
        cls.cfg = read_config_file(CONFIG)

        # Create webdriver
        cls.driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)

        # Start App if not running
        cls._start_app()
        cls._wait_for_app()

    @classmethod
    def tearDownClass(cls):
        # Kill webdriver
        cls.driver.close()

        # Kill app
        cls._stop_app()

    @classmethod
    def _root(cls):
        return "http://%s:%s" % (cls.cfg["web_server"]["host"], cls.cfg["web_server"]["port"])

    @classmethod
    def _req(cls, path, params=None):
        if params:
            return "%s/%s?%s" % (cls._root(), path, params)
        return "%s/%s" % (cls._root(), path)

    @classmethod
    def _start_app(cls):
        if not cls._ping_app():
            os.popen(cls.cfg["executable"])

    @classmethod
    def _wait_for_app(cls):
        timeout = 5
        while timeout > 0 and not cls._ping_app():
            sleep(1)
            timeout -= 1
        if timeout == 0:
            sys.exit('App not running!')

    @classmethod
    def _ping_app(cls):
        try:
            return requests.get(cls._req('')).status_code == 200
        except Exception as ex:
            print str(ex)
            return False

    @classmethod
    def _stop_app(cls):
        os.popen("kill $(ps aux | grep 'test.json' | awk '{print $2}')")