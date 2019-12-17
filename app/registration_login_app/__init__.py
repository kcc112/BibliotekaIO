from flask import Blueprint

registration_login_app = Blueprint('registration_login_app', __name__)

from . import registration_login
