import argparse
import os
from threading import Thread
from database import Database
from flask_pymongo import MongoClient
from utils import setup_logger, read_json_file

def run():
    # Argument parser
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-m") # Config arg
    args = arg_parser.parse_known_args()
    test_mode = hasattr(args[0], 'm') and args[0].m == 'test'

    # Config
    cfg = read_json_file(os.environ["SPONGE_CFG"] if not test_mode else os.environ["SPONGE_TEST_CFG"])

    # Logging
    setup_logger(cfg["logging"]["file"], cfg["logging"]["level"])

    # DB
    db_client = MongoClient(cfg["database"]["host"], cfg["database"]["port"])
    db_wrapper = Database(db_client[cfg["database"]["name"]], cfg)

    # Web Server
    if cfg["web_server"]["enabled"]:
        import views
        views.db = db_wrapper
        views.app.template_folder = cfg["web_server"]["template_folder"]
        Thread(target=views.app.run, args=(cfg["web_server"]["host"], cfg["web_server"]["port"])).start()

if __name__ == "__main__":
    run()