from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..models import User
from . import example_app
from .forms import NameForm
from datetime import date


@example_app.route('/getWorkers')
def getWorkers():
    return render_template('example_app/getWorkersView.html',
                           users=User.query.order_by(User.id.desc()).all()
                           )
