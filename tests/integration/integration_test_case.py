import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from test_case import SpongeTestCase
import requests
from time import sleep

class SpongeIntegrationTestCase(SpongeTestCase):

    @classmethod
    def setUpClass(cls):
        super(SpongeIntegrationTestCase, cls).setUpClass()
        cls._start_app()
        cls._wait_for_app()

    @classmethod
    def tearDownClass(cls):
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