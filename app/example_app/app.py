from flask import Flask, render_template, request, redirect, url_for
import datetime
from .. import db
from ..models import Event, User, Auditorium
from . import example_app

@example_app.route('/')
def home():
    return render_template('eventTemplates/index.html')


@example_app.route('/user')
def user_site():
    return render_template('eventTemplates/user.html')


@example_app.route('/admin')
def admin_site():
    return render_template('eventTemplates/admin.html')


# to tylko wstepne ale nie ogarniam bazy totalnie czy to jest git w
# przypadku jak relacje bo to by była ta sama metoda dla kazdej tabeli xdd
@example_app.route('/admin/add-event', methods=['GET', 'POST'])
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
        return redirect(url_for('get_all_event'))
    return render_template('eventTemplates/add_event.html', auditoriums=Auditorium.query.all())


@example_app.route('/admin/delete-event/<id>')
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('get_all_event'))


@example_app.route('/admin/get-event/<id>')
def get_event(id):
    return render_template('eventTemplates/event.html',
                           event=Event.query.get_or_404(id)
                           )


@example_app.route('/admin/all-events')
def get_all_event():
    return render_template('eventTemplates/all-events.html',
                           events=Event.query.order_by(Event.id.desc()).all()
                           )


@example_app.route('/admin/auditorium')
def get_all_auditoriums():
    return render_template('eventTemplates/all-auditoriums.html',
                           auditoriums=Auditorium.query.order_by(Auditorium.number).all()
                           )


@example_app.route('/admin/get-auditorium/<id>')
def get_auditorium(id):
    return render_template('eventTemplates/auditorium.html',
                           auditorium=Auditorium.query.get_or_404(id)
                           )


@example_app.route('/admin/add-auditorium', methods=['GET', 'POST'])
def add_auditorium():
    if request.method == 'POST':
        auditorium = Auditorium(id=request.form['id'], maxPlaces=request.form['maxPlaces'], number=request.form['number'])
        db.session.add(auditorium)
        db.session.commit()
        return redirect(url_for('get_all_auditoriums'))
    return render_template('eventTemplates/add_auditorium.html')


#if __name__ == '__main__':
 #   example_app.run()
