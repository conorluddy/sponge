from flask import request, render_template
from utils import json_response, monitor, load_config
from flask import Flask
from flask.ext.autodoc import Autodoc

template_folder = load_config()['web_server']['template_folder']
app = Flask(__name__, static_url_path='', template_folder=template_folder)
documentor = Autodoc(app)
db = None # DB Wrapper Placeholder

@monitor
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

#TODO - authenticate requests
@monitor
@app.route('/')
@documentor.doc()
def index():
    return render_template('index.html')

#### User ####

@monitor
@app.route('/user')
@documentor.doc()
def user():
    return json_response(db.get("user", request.args.get("uuid")))

@monitor
@app.route('/user/add', methods=['POST'])
@documentor.doc()
def user_add():
    return json_response(
        db.insert_user(
            uuid=request.form.get("uuid"),
            mail=request.form["mail"],
            name=request.form["name"],
            password=request.form["password"],
            intro=request.form["intro"],
        )
    )

@monitor
@app.route('/user/remove')
@documentor.doc()
def user_remove():
    return json_response(db.remove_user(request.args.get("uuid")))

#### Item ####

@monitor
@app.route('/item')
@documentor.doc()
def item():
    return json_response(db.get("item", request.args.get("uuid")))

@monitor
@app.route('/item/add', methods=['POST'])
@documentor.doc()
def item_add():
    return json_response(
        db.insert_item(
            title=request.form.get("title"),
            description=request.form.get("description"),
            category=request.form.get("category"),
            lender=request.form.get("lender"),
            published=request.form.get("published", False),
            day_rate=request.form.get("day_rate"),
            week_rate=request.form.get("week_rate"),
            month_rate=request.form.get("month_rate"),
            mon=request.form.get("mon", True),
            tue=request.form.get("tue", True),
            wed=request.form.get("wed", True),
            thu=request.form.get("thu", True),
            fri=request.form.get("fri", True),
            sat=request.form.get("sat", True),
            sun=request.form.get("sun", True),
            attributes=request.form.get("attributes")
        )
    )

@monitor
@app.route('/item/remove')
@documentor.doc()
def item_remove():
    return json_response(db.remove("item", request.args.get("uuid")))

#### Contract ####

@monitor
@app.route('/contract')
@documentor.doc()
def contract():
    return json_response(db.get("contract", request.args.get("uuid")))

@monitor
@app.route('/contract/add', methods=['POST'])
@documentor.doc()
def contract_add():
    return json_response(
        db.insert_contract(
            item=request.form["item"],
            borrower=request.form["borrower"],
            lender=request.form["lender"],
            start_date=request.form["start_date"],
            end_date=request.form["end_date"],
            cost=request.form["cost"],
            confirmed=request.args.get("confirmed", False),
            cancelled=request.args.get("cancelled", False)
        )
    )

@monitor
@app.route('/contract/confirm')
@documentor.doc()
def contract_confirm():
    return json_response(
        db.confirm_contract(
            uuid=request.args.get("uuid"),
            lender=request.args.get("lender")
        )
    )

@monitor
@app.route('/contract/remove')
@documentor.doc()
def contract_remove():
    return json_response(db.remove("contract", request.args.get("uuid")))
