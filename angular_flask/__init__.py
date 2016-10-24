from datetime import timedelta
from flask import Flask
from angular_flask.constants import SESSION_DURATION_SECONDS

app = Flask(__name__)

app.config.from_object('angular_flask.settings')

app.url_map.strict_slashes = False

app.permanent_session_lifetime = timedelta(seconds=SESSION_DURATION_SECONDS)

import angular_flask.core
import angular_flask.models
import angular_flask.controllers
import angular_flask.utils
