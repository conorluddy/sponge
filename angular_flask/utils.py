import json
from functools import wraps
import gpxpy.geo
from flask import request

def geoDistance(lat1, lng1, lat2, lng2):
    return gpxpy.geo.haversine_distance(lat1, lng1, lat2, lng2)

def geoDistanceString(dist):
    if dist > 1000:
        return str(int(dist / 1000)) + "km"
    return "~" + str(int(dist)) + "m"

def parse_args(method='post', string_args=None, int_args=None, float_args=None, json_args=None, bool_args=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):

            if method == 'get':
                input = request.args
            elif request.data:
                input = json.loads(request.data)
            else:
                input = {}

            output = {}
            for key in string_args or []:
                output[key] = input.get(key)

            for key in int_args or []:
                output[key] = int(input.get(key, 0))

            for key in float_args or []:
                output[key] = float(input.get(key, 0))

            for key in json_args or []:
                input_json = input.get(key)
                output[key] = json.loads(input_json) if input_json else input_json

            for key in bool_args or []:
                output[key] = bool(input.get(key, False))

            return test_func(output, *args, **kwargs)
        return wrapper
    return actualDecorator