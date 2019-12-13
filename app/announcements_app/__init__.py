from flask import Blueprint

announcements_app = Blueprint('announcements_app', __name__)

from . import announcement_board