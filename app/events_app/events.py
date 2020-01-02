from flask import Flask, render_template, request, redirect, url_for
import datetime
from .. import db
from ..models import Event, User, Auditorium
from . import events_app
from app.registration_login_app.registration_login import required_roles


@events_app.route('/event/home')
def home():
    return render_template('/events/index.html')


@events_app.route('/user')
def user_site():
    return render_template('/events/user.html')


@events_app.route('/admin')
@required_roles('admin')
def admin_site():
    return render_template('/events/admin.html')


# to tylko wstepne ale nie ogarniam bazy totalnie czy to jest git w
# przypadku jak relacje bo to by była ta sama metoda dla kazdej tabeli xdd
@events_app.route('/admin/add-event', methods=['GET', 'POST'])
# def add_event(event):
#     db.session.add(event)
#     db.session.commit()
def add_event():
    if request.method == 'POST':
        data = datetime.datetime(*[int(v) for v in request.form['date'].replace('T', '-').replace(':', '-').split('-')])
        event = Event(id=request.form['id'], name=request.form['name'], description=request.form['desc'],
                      date=data, auditorium=request.form['auditorium'])
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events_app.get_all_event'))
    return render_template('/events/add_event.html', auditoriums=Auditorium.query.all())


@events_app.route('/admin/delete-event/<id>')
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('events_app.get_all_event'))


@events_app.route('/admin/get-event/<id>')
def get_event(id):
    return render_template('/events/event.html',
                           event=Event.query.get_or_404(id)
                           )


@events_app.route('/admin/all-events')
def get_all_event():
    return render_template('/events/all-events.html',
                           events=Event.query.order_by(Event.id.desc()).all()
                           )


@events_app.route('/admin/auditorium')
def get_all_auditoriums():
    return render_template('/events/all-auditoriums.html',
                           auditoriums=Auditorium.query.order_by(Auditorium.number).all()
                           )


@events_app.route('/admin/get-auditorium/<id>')
def get_auditorium(id):
    return render_template('/events/auditorium.html',
                           auditorium=Auditorium.query.get_or_404(id)
                           )


@events_app.route('/admin/add-auditorium', methods=['GET', 'POST'])
def add_auditorium():
    if request.method == 'POST':
        auditorium = Auditorium(id=request.form['id'], maxPlaces=request.form['maxPlaces'], number=request.form['number'])
        db.session.add(auditorium)
        db.session.commit()
        return redirect(url_for('events_app.get_all_auditoriums'))
    return render_template('/events/add_auditorium.html')


#if __name__ == '__main__':
 #   example_app.run()
