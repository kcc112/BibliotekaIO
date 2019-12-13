from flask import Blueprint

example_app = Blueprint('example_app', __name__)

from . import views, errors, books
