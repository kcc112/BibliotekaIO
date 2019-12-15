from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from . import app
from .forms import NameForm


@app.route('/')
def index():
    return render_template('app/index.html')
