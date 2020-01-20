from flask import Flask, render_template, request, redirect, url_for
import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField, DateTimeLocalField, DateTimeField
from wtforms.validators import DataRequired

from .. import db
from ..models import Event, User, Auditorium
from . import events_app
from app.registration_login_app.registration_login import required_roles
from flask_login import login_required


@events_app.route('/event/user')
@required_roles('employee', 'client')
@login_required
def user_site():
    #dodać wybranie przypisanych eventów
    return render_template('/events/user.html', events=Event.query.order_by(Event.id.desc()).all())


@events_app.route('/event/admin')
#@required_roles('admin')
@login_required
def admin_site():
    return render_template('/events/admin.html')


@events_app.route('/event/admin/add-event', methods=['GET', 'POST'])
#@required_roles('admin')
@login_required
def add_event():
    dateform = EventDateForm()
    if request.method == 'POST':
    # data = datetime.datetime(*[int(v) for v in request.form['date'].replace('T', '-').replace(':', '-').split('-')])
        event = Event(id=request.form['id'], name=request.form['name'], description=request.form['desc'],
                      date=dateform.start_date.data, auditorium=request.form['auditorium'])
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events_app.get_all_event'))
    return render_template('/events/add_event.html', auditoriums=Auditorium.query.all(), dateform=dateform)


@events_app.route('/event/admin/delete-event/<id>')
#@required_roles('admin')
@login_required
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('events_app.get_all_event'))


@events_app.route('/event/admin/get-event/<id>')
#@required_roles('admin')
@login_required
def get_event(id):
    return render_template('/events/event.html',
                           event=Event.query.get_or_404(id)
                           )


@events_app.route('/event/admin/all-events')
#@required_roles('admin')
@login_required
def get_all_event():
    return render_template('/events/all-events.html',
                           events=Event.query.order_by(Event.id.desc()).all()
                           )


@events_app.route('/event/admin/auditorium')
#@required_roles('admin')
@login_required
def get_all_auditoriums():
    return render_template('/events/all-auditoriums.html',
                           auditoriums=Auditorium.query.order_by(Auditorium.number).all()
                           )


@events_app.route('/event/admin/get-auditorium/<id>')
#@required_roles('admin')
@login_required
def get_auditorium(id):
    return render_template('/events/auditorium.html',
                           auditorium=Auditorium.query.get_or_404(id)
                           )


@events_app.route('/event/admin/add-auditorium', methods=['GET', 'POST'])
#@required_roles('admin')
@login_required
def add_auditorium():
    if request.method == 'POST':
        auditorium = Auditorium(id=request.form['id'], maxPlaces=request.form['maxPlaces'], number=request.form['number'])
        db.session.add(auditorium)
        db.session.commit()
        return redirect(url_for('events_app.get_all_auditoriums'))
    return render_template('/events/add_auditorium.html')


@events_app.route('/event/admin/assign-to-user/<id>', methods=['GET', 'POST'])
#@required_roles('admin')
@login_required
def assign_to_user():
    if request.method == 'POST':
        event = Event.query.get_or_404(id)
        user = User.query.get_or_404(id=request.form['user_id'])
        #many2many =
        #teraz tutaj zrobic przypisywanie uzytkownika do wydarzenia z html form gdzie wybiera sie
        #uzytkownika z selecta jak te audytoria
        #event.
        #tu zapis
        return redirect(url_for('events_app.get_all_auditoriums'))
    return render_template('/events/assign-to-user.html', events=Event.query().all(), users=User.query().all())



class EventDateForm(FlaskForm):
    #dt = DateField('DatePicker', format='%Y-%m-%d', default=date.today())
    start_date = DateTimeField(
        'DatePicker', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime.now())
    submit = SubmitField('Submit', validators=[DataRequired()])