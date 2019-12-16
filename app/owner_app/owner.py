from flask import render_template, session, redirect, url_for, request, flash
from .. import db
from ..models import User, WorkSchedule
from . import owner_app
from ..registration_login_app import forms
import datetime


@owner_app.route('/ownerModule/ownerView')
def ownerView():
    return render_template('/owner/ownerView.html')


@owner_app.route('/ownerModule/getWorkers')
def getWorkers():
    return render_template('owner/getWorkersView.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/ownerModule/getWorkSchedules')
def getWorkSchedules():
    return render_template('owner/workSchedules.html', workSchedules=WorkSchedule.query.order_by(WorkSchedule.id.desc()).all())


@owner_app.route('/ownerModule/addWorkSchedule', methods=['GET', 'POST'])
def addWorkSchedule():
    if request.method == 'POST':
        workSchedule = WorkSchedule(day=request.form['day'],startTime=datetime.time(int(request.form['start_time'].split(":")[0]), int(request.form['start_time'].split(":")[1])),endTime=datetime.time(int(request.form['end_time'].split(":")[0]), int(request.form['end_time'].split(":")[1])),worker_id=request.form['worker_id'])

        db.session.add(workSchedule)
        db.session.commit()
        return redirect(url_for('owner_app.getWorkSchedules'))
    return render_template('owner/addWorkSchedule.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/ownerModule/deleteWorkSchedule/<id>')
def deleteWorkSchedule(id):
    db.session.delete(WorkSchedule.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('owner_app.getWorkSchedules'))


@owner_app.route('/ownerModule/editWorkSchedule/<id>', methods=['GET', 'POST'])
def editWorkSchedule(id):
    workSchedule = WorkSchedule.query.get(id)
    if request.method == 'POST':
        workSchedule.day = request.form['day']
        workSchedule.startTime = datetime.time(int(request.form['start_time'].split(":")[0]), int(request.form['start_time'].split(":")[1]))
        workSchedule.endTime = datetime.time(int(request.form['end_time'].split(":")[0]), int(request.form['end_time'].split(":")[1]))
        workSchedule.worker_id = request.form['worker_id']
        db.session.commit()
        return redirect(url_for('owner_app.getWorkSchedules'))
    return render_template('owner/editWorkSchedule.html', workSchedule=workSchedule, users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/ownerModule/addWorker', methods=['GET', 'POST'])
def addWorker():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, user_type='employee')
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('The new employee has been added!')
        return redirect(url_for('owner_app.getWorkers'))
    return render_template('/owner/addWorkerView.html', title='Register', form=form)


@owner_app.route('/ownerModule/deleteWorker/<id>')
def deleteWorker(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('owner_app.getWorkers'))
