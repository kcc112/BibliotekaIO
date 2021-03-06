from flask import Flask, render_template, request, redirect, url_for
import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from sqlalchemy import exc, and_, or_

from .. import db
from ..models import Event, User, Auditorium, UserEvent
from . import events_app
from app.registration_login_app.registration_login import required_roles
from flask_login import login_required, current_user


@events_app.route('/event/user')
@required_roles('employee', 'client')
@login_required
def user_site():
    result = db.session.query(Event).join(UserEvent).filter(UserEvent.user_id == current_user.id).all()
    audits = db.session.query(Auditorium).join(Event).filter(Auditorium.id == Event.auditorium).join(UserEvent)\
        .filter(UserEvent.user_id == current_user.id).all()
    sums = []
    for i in result:
        sums.append(len(db.session.query(User).join(UserEvent).filter(UserEvent.event_id == i.id).all()))
    return render_template('/events/user.html', events=result, audits=audits, users=sums, size=len(result))


@events_app.route('/event/admin')
@required_roles('admin')
@login_required
def admin_site():
    return render_template('/events/admin.html')


@events_app.route('/event/admin/add-event', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def add_event():
    dateform = EventDateForm()
    if request.method == 'POST':
        event = Event(id=request.form['id'], name=request.form['name'], description=request.form['desc'],
                      date=dateform.start_date.data, endDate=dateform.end_date.data,
                      auditorium=request.form['auditorium'])
        if check_dates(event) == 0:
            db.session.add(event)
            db.session.commit()
        return redirect(url_for('events_app.get_all_event'))
    return render_template('/events/add_event.html', auditoriums=Auditorium.query.all(), dateform=dateform)


@events_app.route('/event/admin/modify-event/<id>', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def modify_event(id):
    event = Event.query.get_or_404(id)
    dateform = EventDateForm()
    if request.method == 'POST' & check_dates(event) == 0:
        event.name = request.form['name']
        event.description = request.form['desc']
        event.date = dateform.start_date.data
        event.endDate = dateform.end_date.data
        event.auditorium = request.form['auditorium']
        db.session.commit()
        print(request.form)
        return redirect(url_for('events_app.get_all_event'))
    dateform.start_date.data = event.date
    dateform.end_date.data = event.endDate
    return render_template('/events/modify_event.html', auditoriums=Auditorium.query.all(), dateform=dateform, eventForm=event)


@events_app.route('/event/admin/delete-event/<id>')
@required_roles('admin')
@login_required
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('events_app.get_all_event'))


@events_app.route('/event/admin/get-event/<id>')
@required_roles('admin')
@login_required
def get_event(id):
    return render_template('/events/event.html',
                           event=Event.query.get_or_404(id)
                           )


@events_app.route('/event/admin/all-events')
@required_roles('admin')
@login_required
def get_all_event():
    return render_template('/events/all-events.html',
                           events=Event.query.order_by(Event.id.desc()).all()
                           )


@events_app.route('/event/admin/auditorium')
@required_roles('admin')
@login_required
def get_all_auditoriums():
    return render_template('/events/all-auditoriums.html',
                           auditoriums=Auditorium.query.order_by(Auditorium.number).all()
                           )


@events_app.route('/event/admin/get-auditorium/<id>')
@required_roles('admin')
@login_required
def get_auditorium(id):
    return render_template('/events/auditorium.html',
                           auditorium=Auditorium.query.get_or_404(id)
                           )


@events_app.route('/event/admin/add-auditorium', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def add_auditorium():
    if request.method == 'POST':
        auditorium = Auditorium(id=request.form['id'], maxPlaces=request.form['maxPlaces'], number=request.form['number'])
        db.session.add(auditorium)
        db.session.commit()
        return redirect(url_for('events_app.get_all_auditoriums'))
    return render_template('/events/add_auditorium.html')


@events_app.route('/event/admin/assign-to-user/<id>', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def assign_to_user(id):
    event = Event.query.get_or_404(id)
    user = AssignForm(request.form)
    user.choose.choices = [(u.id, u.email) for u in User.query.all()]
    # ile uzytkownikow idzie na event
    user_check = UserEvent.query.filter(UserEvent.event_id == id).all()
    audit_check = Auditorium.query.filter(Auditorium.id == event.auditorium).first()
    if request.method == 'POST':
        if audit_check.maxPlaces > len(user_check):
            for f in user.choose.data:
                user_event = UserEvent(user_id=f, event_id=id)
                try:
                    db.session.add(user_event)
                    db.session.commit()
                except exc.IntegrityError as e:
                    db.session().rollback()
            return redirect(url_for('events_app.get_all_event'))
    userEvent = db.session.query(User).join(UserEvent).filter(UserEvent.event_id == event.id).all()
    return render_template('/events/assign-to-user.html', event=event, users=user, userEvent=userEvent)


def check_dates(event):
    conds = [Event.date >= event.date, Event.date <= event.endDate]
    conds2 = [Event.endDate >= event.date, Event.endDate <= event.endDate]
    conds3 = [Event.date <= event.date, Event.endDate >= event.endDate]
    res = Event.query.filter(Event.auditorium == event.auditorium).filter(
        or_(and_(*conds), and_(*conds2), and_(*conds3))).all()
    return len(res)


class EventDateForm(FlaskForm):
    start_date = DateTimeField(
        'DatePicker', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime.now())
    end_date = DateTimeField('DatePicker', format='%Y-%m-%d %H:%M:%S',
         default=datetime.datetime.now() + datetime.timedelta(hours=7))
    submit = SubmitField('Submit', validators=[DataRequired()])


class AssignForm(FlaskForm):
    choose = SelectMultipleField(u'Users', coerce=int)
