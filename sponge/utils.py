from flask import make_response
from uuid import uuid4, uuid5, NAMESPACE_DNS
from logging.handlers import RotatingFileHandler
import logging
import json
import re
import os

def load_config():
    return read_json_file(os.environ['SPONGE_CFG'])

def load_test_config():
    return read_json_file(os.environ['SPONGE_TEST_CFG'])

def read_json_file(config_file):
    with open(config_file, "r") as f:
        cfg_json = json.loads(f.read())
    return cfg_json

def list_to_title_string(list):
    string = ""
    for item in list:
        string += item.title() + ", "
    return string[0:len(string) - 2]

def make_uuid(string):
    return str(uuid5(NAMESPACE_DNS, string))

def random_uuid():
    return str(uuid4())

def extract_uuid(string):
    regex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
    result = regex.findall(string)
    return result[0] if result else None

def wrapped_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception, e:
        logging.error("Fatal error calling %s" % str(func), exc_info=True)

def raw_response(response_string):
    response = make_response(response_string)
    response.mimetype = "text/plain"
    return response

def json_response(response, count=None, sort=False):
    if sort and type(response) is list:
        response = sorted(response)
    if count is not None:
        response = make_response(json.dumps({"count": count, "data": response}))
    else:
        response = make_response(json.dumps(response))
    response.mimetype = "application/json"
    return response

def setup_logger(log_file, log_level):
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=2) # File handler
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:[%(module)s:%(lineno)d]:[%(threadName)s]:%(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    ch = logging.StreamHandler() # Stream handler
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def strip_dict(dictionary):
    return dict((k, v) for k, v in dictionary.iteritems() if v not in [None, {}, []] and k not in [None, {}, []])

def float_to_two_places(x):
    return int(x * 100) / 100.0

def capitalise(string):
    return string.title()

def monitor(fn):
    def wrapped(*v, **k):
        # logging.info("Mon: %s %s" % (fn.__name__, str(v)))
        return fn(*v, **k)
    return wrapped

if __name__ == "__main__":
    print extract_uuid('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">"791996c3-de0b-5632-90bd-abf6b045c5ba"</pre></body></html>')
    print extract_uuid('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;"></pre></body></html>')