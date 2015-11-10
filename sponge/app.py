import argparse
from threading import Thread
from database import Database
from cleaner import Cleaner
from flask_pymongo import MongoClient
from utils import setup_logger, read_config_file

def run():
    # Argument parser
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c") # Config arg
    args = arg_parser.parse_known_args()
    config_path = args[0].c

    # Config
    cfg = read_config_file(config_path)

    # Logging
    setup_logger(cfg["logging"]["file"], cfg["logging"]["level"])

    # DB
    db_client = MongoClient(cfg["database"]["host"], cfg["database"]["port"])
    db_wrapper = Database(db_client[cfg["database"]["name"]])

    # Cleaner
    if cfg["cleaner"]["enabled"]:
        Thread(target=Cleaner(cfg["cleaner"]["frequency"], db_wrapper).run).start()

    # Web Server
    if cfg["web_server"]["enabled"]:
        import views
        views.db = db_wrapper
        Thread(target=views.app.run, args=(cfg["web_server"]["host"], cfg["web_server"]["port"])).start()

if __name__ == "__main__":
    run()