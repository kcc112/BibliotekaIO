from flask import Blueprint

owner_app = Blueprint('owner_app', __name__)

from . import owner, errors