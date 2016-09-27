import logging
from crontab import CronTab
import time

class Cleaner(object):

    def __init__(self, frequency, db_wrapper):
        self.cron = CronTab(frequency)
        self.db = db_wrapper

    def run(self):
        logging.info("Cleaner Running")
        while True:
            time.sleep(self.cron.next())
            self._remove_stale_data()

    def _remove_stale_data(self):
        pass
        # self.db.remove("pizza", {"stamp": {"$lt": stale_data_cutoff}})
        # self.db.remove("sides", {"stamp": {"$lt": stale_data_cutoff}})
