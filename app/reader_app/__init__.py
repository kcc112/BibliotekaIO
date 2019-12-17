from flask import Blueprint

reader_app = Blueprint('reader_app', __name__)

from . import reader, books

