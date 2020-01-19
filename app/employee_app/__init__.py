from flask import Blueprint

employee_app = Blueprint('employee_app', __name__)

from . import employee
