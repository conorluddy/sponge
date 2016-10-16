import json
import os
from functools import wraps

import flask
from flask import render_template, send_from_directory
from flask import request

from services import CategoryService, CountyService, ItemService
from angular_flask.core import api_manager
from angular_flask.models import *

session = api_manager.session

def parse_args(method='post', string_args=None, int_args=None, float_args=None, json_args=None, bool_args=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            input = request.args if method == 'get' else json.loads(request.data)
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

### Services ###

item_service = ItemService()
category_service = CategoryService()
county_service = CountyService()

counties = county_service.get()['results']

### Pages ###

@app.route('/')
@app.route('/about')
@app.route('/blog')
@app.route('/search')
def basic_pages(**kwargs):
    return render_template('index.html', **{'counties': counties})

### API ###

@app.route('/api/item', methods=['POST'])
@parse_args(
    string_args=['title', 'description', 'address', 'image'],
    int_args=['day_rate', 'lender', 'category', 'county_id'],
    float_args=['lat', 'lng']
)
def item_post(item):
    item_service.post(item)
    return "Added", 200

@app.route('/api/item', methods=['DELETE'])
@parse_args(
    int_args=['id']
)
def item_delete(input):
    item_service.delete(input['id'])
    return "Deleted", 200

@app.route('/api/item', methods=['PATCH'])
@parse_args(
    string_args=['title', 'description', 'address', 'image'],
    bool_args=['published'],
    int_args=['id', 'day_rate', 'lender', 'category']
)
def item_patch(item):
    item_service.patch(item)
    return "Updated", 200

@app.route('/api/item', methods=['GET'])
@parse_args(
    method='get',
    int_args=['id', 'category', 'page', 'county'],
    string_args=['search']
)
def item_get(input):
    return flask.jsonify(**item_service.get(
        id=input.get('id'),
        search=input.get('search'),
        category=input.get('category'),
        page=input.get('page'),
        county=input.get('county'),
        lat=float(request.cookies.get('sponge_lat', 0.0)),
        lng=float(request.cookies.get('sponge_lng', 0.0))
    ))

@app.route('/api/category', methods=['GET'])
def category_get():
    return flask.jsonify(**category_service.get())

@app.route('/api/category', methods=['POST'])
@parse_args(
    string_args=['name', 'image'],
    int_args=['count']
)
def category_post(category):
    category_service.post(category)
    return "Added", 200

@app.route('/api/county', methods=['GET'])
def county_get():
    return flask.jsonify(**county_service.get())

@app.route('/api/county', methods=['POST'])
@parse_args(
    string_args=['name']
)
def county_post(county):
    county_service.post(county)
    return "Added", 200

### Other ###

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404