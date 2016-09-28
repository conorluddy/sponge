import os
import json
from functools import wraps

from services import ItemService

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from angular_flask import app

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.core import api_manager
from angular_flask.models import *


"""
def auth(permissions=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):

            session['stamp'] = time()
            if session.get('user_id') is None:
                session.clear()
                abort(403, 'You are no longer logged in!')

            user_permissions = db_wrapper.permissions_get(session['user_id'])
            for permission in permissions or []:
                if not user_permissions or permission not in user_permissions:
                    abort(400, "You don't have permission to do this!")

            return test_func(*args, **kwargs)
        return wrapper
    return actualDecorator
"""

def parse_args(string_args=None, int_args=None, json_args=None, bool_args=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            input = json.loads(request.data)
            output = {}
            for key in string_args or []:
                output[key] = input.get(key)

            for key in int_args or []:
                output[key] = int(input.get(key, 0))

            for key in json_args or []:
                input_json = input.get(key)
                output[key] = json.loads(input_json) if input_json else input_json

            for key in bool_args or []:
                output[key] = bool(input.get(key, False))

            return test_func(output, *args, **kwargs)
        return wrapper
    return actualDecorator

"""
for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST'])
"""

item_service = ItemService()

session = api_manager.session

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
@app.route('/blog')
def basic_pages(**kwargs):
    return make_response(open('angular_flask/templates/index.html').read())

# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']


"""
@app.route('/<model_name>/')
@app.route('/<model_name>/<item_id>')
def rest_pages(model_name, item_id=None):
    if model_name in crud_url_models:
        model_class = crud_url_models[model_name]
        if item_id is None or session.query(exists().where(
                model_class.id == item_id)).scalar():
            return make_response(open(
                'angular_flask/templates/index.html').read())
    abort(404)
"""

@app.route('/item', methods=['POST'])
@parse_args(string_args=['title', 'description'], int_args=['day_rate', 'lender', 'category'])
def item_post(item):
    item_service.post(item)
    return "Added", 200

@app.route('/item', methods=['DELETE'])
@parse_args(int_args=['id'])
def item_delete(input):
    item_service.delete(input['id'])
    return "Deleted", 200

# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
