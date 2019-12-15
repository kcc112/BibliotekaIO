from flask import Blueprint

main_app = Blueprint('main_app', __name__)

from . import main
