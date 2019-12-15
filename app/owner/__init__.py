from flask import Blueprint

owner = Blueprint('owner', __name__)

from . import OwnerService, views, errors