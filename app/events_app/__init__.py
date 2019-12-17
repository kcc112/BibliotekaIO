from flask import Blueprint

events_app = Blueprint('events_app', __name__)

from . import events