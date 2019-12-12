from flask import render_template, request, session, redirect, url_for, current_app
from .. import db
from ..models import User
from . import example_app
from .forms import NameForm


@example_app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('example_app/index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

