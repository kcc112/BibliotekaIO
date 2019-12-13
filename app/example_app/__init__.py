from flask import Blueprint

example_app = Blueprint('example_app', __name__)

from . import announcement_board