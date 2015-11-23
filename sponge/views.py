from flask import request, render_template
from utils import json_response
from objects.user import User
from flask import Flask
from flask.ext.autodoc import Autodoc

app = Flask(__name__, static_url_path='')
documentor = Autodoc(app)
db = None # DB Wrapper Placeholder

@app.route('/docs')
@documentor.doc()
def docs():
    """
    Get API documentation
    """
    return documentor.html(
        title="Sponge",
        author="ianluddy@gmail.com"
    )

#TODO - authenticate api calls
@app.route('/')
@documentor.doc()
def index():
    return render_template('index.html')

#### User ####

@app.route('/user')
@documentor.doc()
def user():
    return json_response(db.get("user", request.args.get("uuid")))

@app.route('/user/add')
@documentor.doc()
def user_add():
    return json_response(
        db.insert_user(
            uuid=request.args.get("uuid"),
            mail=request.args.get("mail"),
            first=request.args.get("first"),
            last=request.args.get("last"),
            password=request.args.get("password"),
            intro=request.args.get("intro"),
        )
    )

@app.route('/user/remove')
@documentor.doc()
def user_remove():
    return json_response(db.remove_user(request.args.get("uuid")))

#### Item ####

@app.route('/item')
@documentor.doc()
def item():
    return json_response(db.get("item", request.args.get("uuid")))

@app.route('/item/add')
@documentor.doc()
def item_add():
    return json_response(
        db.insert_item(
            title=request.args.get("title"),
            description=request.args.get("description"),
            lender=request.args.get("lender"),
            published=request.args.get("published", False),
            day_rate=request.args.get("day_rate"),
            week_rate=request.args.get("week_rate"),
            month_rate=request.args.get("month_rate"),
            mon=request.args.get("mon", True),
            tue=request.args.get("tue", True),
            wed=request.args.get("wed", True),
            thu=request.args.get("thu", True),
            fri=request.args.get("fri", True),
            sat=request.args.get("sat", True),
            sun=request.args.get("sun", True),
            attributes=request.args.get("attributes")
        )
    )

@app.route('/item/remove')
@documentor.doc()
def item_remove():
    return json_response(db.remove("item", request.args.get("uuid")))
