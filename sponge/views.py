from flask import request, render_template
from utils import json_response
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

#TODO - authenticate requests
@app.route('/')
@documentor.doc()
def index():
    return render_template('index.html')

#### User ####

@app.route('/user')
@documentor.doc()
def user():
    return json_response(db.get("user", request.args.get("uuid")))

@app.route('/user/add', methods=['POST'])
@documentor.doc()
def user_add():
    return json_response(
        db.insert_user(
            uuid=request.form.get("uuid"),
            mail=request.form["mail"],
            first=request.form["first"],
            last=request.form["last"],
            password=request.form["password"],
            intro=request.form["intro"],
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

@app.route('/item/add', methods=['POST'])
@documentor.doc()
def item_add():
    return json_response(
        db.insert_item(
            title=request.form["title"],
            description=request.form.get("description"),
            lender=request.form["lender"],
            published=request.form.get("published", False),
            day_rate=request.form["day_rate"],
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

@app.route('/item/remove')
@documentor.doc()
def item_remove():
    return json_response(db.remove("item", request.args.get("uuid")))

#### Contract ####

@app.route('/contract')
@documentor.doc()
def contract():
    return json_response(db.get("contract", request.args.get("uuid")))

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

@app.route('/contract/confirm')
@documentor.doc()
def contract_confirm():
    return json_response(
        db.confirm_contract(
            uuid=request.args.get("uuid"),
            lender=request.args.get("lender")
        )
    )

@app.route('/contract/remove')
@documentor.doc()
def contract_remove():
    return json_response(db.remove("contract", request.args.get("uuid")))
