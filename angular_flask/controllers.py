import os
import flask
from flask import render_template, send_from_directory
from flask import request, jsonify
from services import CategoryService, CountyService, ItemService, UserService, ApiException
from angular_flask.core import api_manager
from angular_flask.models import *
from angular_flask.utils import parse_args

session = api_manager.session

### Exceptions ###

@app.errorhandler(ApiException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

### Services ###

item_service = ItemService()
user_service = UserService()
category_service = CategoryService()
county_service = CountyService()

counties = county_service.get()['results']

### Pages ###

@app.route('/')
@app.route('/search')
@app.route('/item')
@app.route('/profile')
@app.route('/borrowing')
@app.route('/lending')
def basic_pages():
    return render_template('index.html', **{'counties': counties, 'session': user_service.get_session()})

### API ###

# Item

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
    return "Added", 200

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
    return "Added", 200

# User

@app.route('/api/user/register', methods=['POST'])
@parse_args(
    string_args=['first', 'last', 'email', 'password']
)
def user_register(input):
    user_service.register(input)
    return "Registered", 200

@app.route('/api/user/logout', methods=['GET'])
def user_logout():
    user_service.logout()
    return "Logged Out", 200

@app.route('/api/user/password', methods=['POST'])
@parse_args(
    string_args=['current', 'new']
)
def user_change_password(input):
    user_service.change_password(input)
    return "Updated", 200

@app.route('/api/user/login', methods=['POST'])
@parse_args(
    string_args=['email', 'password']
)
def user_login(input):
    user_service.login(input)
    return "Logged In", 200

@app.route('/api/user', methods=['POST'])
@parse_args(
    string_args=['first', 'last', 'email', 'password', 'photo', 'phone', 'intro'],
)
def user_post(input):
    user_service.post(input)
    return "Added", 200

@app.route('/api/user', methods=['PATCH'])
@parse_args(
    string_args=['first', 'last', 'email', 'photo', 'phone', 'intro', 'dob'],
)
def user_patch(input):
    user_service.patch(input)
    return "Updated", 200

@app.route('/api/user', methods=['GET'])
def user_get():
    return flask.jsonify(**user_service.get())

### Other ###

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404