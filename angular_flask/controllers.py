import os
import flask
import json
from flask import render_template, send_from_directory
from flask import jsonify, session, request, redirect, url_for
from services import CategoryService, CountyService, ItemService, UserService, ApiException
from angular_flask.models import *
from angular_flask.utils import store_profile_image
from angular_flask.constants import *

from functools import wraps

### Decorators ###

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if API_AUTH_ENABLED and 'user_id' not in session:
            raise ApiException('Please login to continue', 401)
        return f(*args, **kwargs)
    return decorated_function

### Handlers ###

@app.errorhandler(ApiException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.before_request
def check_session():
    session.permanent = True

def validate_session():
    if API_AUTH_ENABLED and 'user_id' not in session:
        return redirect(url_for('root'))

### Services ###

item_service = ItemService()
user_service = UserService()
category_service = CategoryService()
county_service = CountyService()

### Pages ###

@app.route('/')
def root():
    return render_template('index.html', **{'session': user_service.get_session()})

@app.route('/search')
@app.route('/item')
def basic_pages():
    return root()

@app.route('/profile')
@app.route('/borrowing')
@app.route('/lending')
def auth_pages():
    validate_session()
    return root()

@app.route('/item/edit', methods=['GET'])
@parse_args(method='get', int_args=['id'])
def item_edit(input):
    item_service.verify_item_owner(input['id'])
    return auth_pages()

### API ###

# Item

@app.route('/api/item', methods=['POST'])
@login_required
@parse_args(
    string_args=['title', 'description', 'address', 'image'],
    int_args=['day_rate', 'lender', 'category', 'county_id'],
    float_args=['lat', 'lng']
)
def item_post(item):
    item_service.post(item)
    return LISTING_ADDED, 200

@app.route('/api/item', methods=['DELETE'])
@login_required
@parse_args(
    int_args=['id']
)
def item_delete(input):
    item_service.delete(input['id'])
    return LISTING_DELETED, 200

@app.route('/api/item', methods=['PATCH'])
@login_required
@parse_args(
    string_args=['title', 'description', 'address', 'image'],
    bool_args=['published'],
    int_args=['id', 'day_rate', 'lender', 'category']
)
def item_patch(item):
    item_service.patch(item)
    return LISTING_UPDATED, 200

@app.route('/api/item', methods=['GET'])
@parse_args(
    method='get',
    int_args=['id', 'category', 'page', 'county'],
    string_args=['search']
)
def item_get(input):
    return flask.jsonify(**item_service.search(
        id=input.get('id'),
        searchTerm=input.get('search'),
        category=input.get('category'),
        page=input.get('page'),
        county=input.get('county'),
        lat=float(request.cookies.get('lat', 0.0)),
        lng=float(request.cookies.get('lng', 0.0))
    ))

# Category

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
    return ADDED, 200

# County

@app.route('/api/county', methods=['GET'])
def county_get():
    return flask.jsonify(**county_service.get())

@app.route('/api/county', methods=['POST'])
@parse_args(
    string_args=['name']
)
def county_post(county):
    county_service.post(county)
    return ADDED, 200

# User

@app.route('/api/user/register', methods=['POST'])
@parse_args(
    string_args=['first', 'last', 'email', 'password']
)
def user_register(input):
    user_service.register(input)
    return ACCOUNT_CREATED, 200

@app.route('/api/user/logout', methods=['GET'])
def user_logout():
    user_service.logout()
    return LOGGED_OUT, 200

@app.route('/api/user/password', methods=['POST'])
@login_required
@parse_args(
    string_args=['current', 'new']
)
def user_change_password(input):
    user_service.change_password(input)
    return PASSWORD_CHANGED, 200

@app.route('/api/user/login', methods=['POST'])
@parse_args(
    string_args=['email', 'password']
)
def user_login(input):
    user_service.login(input)
    return LOGGED_IN, 200

@app.route('/api/user', methods=['POST'])
@parse_args(
    string_args=['first', 'last', 'email', 'password', 'image', 'phone', 'intro'],
)
def user_post(input):
    user_service.post(input)
    return ADDED, 200

@app.route('/api/user', methods=['PATCH'])
@login_required
@parse_args(
    string_args=['first', 'last', 'email', 'image', 'phone', 'intro', 'dob'],
)
def user_patch(input):
    user_service.patch(input)
    return PROFILE_UPDATED, 200

@app.route('/api/user', methods=['GET'])
@login_required
def user_get():
    return flask.jsonify(**user_service.get())

@app.route('/api/user/image', methods=['POST'])
@login_required
def user_image_post():
    filename = store_profile_image(request.files['file'])
    user_service.patch({"image": filename})
    return PHOTO_UPDATED, 200

@app.route('/api/user/listings', methods=['GET'])
@login_required
def user_listings():
    return flask.jsonify(**item_service.get(session['user_id'], field='lender', many=True))

### Other ###

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404