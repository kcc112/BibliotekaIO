from flask import Blueprint

books_app = Blueprint('books_app', __name__)

from . import books
