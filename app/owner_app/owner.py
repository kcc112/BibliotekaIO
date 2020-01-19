from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required
from .. import db
from ..models import User, WorkSchedule
from . import owner_app
from ..registration_login_app import forms
from app.registration_login_app.registration_login import required_roles
import datetime


@owner_app.route('/ownerModule/ownerView')
@required_roles('admin')
@login_required
def ownerView():
    return render_template('/owner/schedules_or_workers.html')


@owner_app.route('/ownerModule/getWorkers')
@required_roles('admin')
@login_required
def getWorkers():
    return render_template('owner/getWorkersView.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/ownerModule/getWorkSchedules')
@required_roles('admin', 'employee')
@login_required
def getWorkSchedules():
    return render_template('/owner/workSchedules.html', workSchedules=WorkSchedule.query.order_by(WorkSchedule.id.desc()).all())


@owner_app.route('/ownerModule/addWorkSchedule', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def addWorkSchedule():
    if request.method == 'POST':
        workSchedule = WorkSchedule(day=request.form['day'],startTime=datetime.time(int(request.form['start_time'].split(":")[0]), int(request.form['start_time'].split(":")[1])),endTime=datetime.time(int(request.form['end_time'].split(":")[0]), int(request.form['end_time'].split(":")[1])),worker_id=request.form['worker_id'])

        db.session.add(workSchedule)
        db.session.commit()
        return redirect(url_for('owner_app.getWorkSchedules'))
    return render_template('owner/addWorkSchedule.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/ownerModule/deleteWorkSchedule/<id>')
@required_roles('admin')
@login_required
def deleteWorkSchedule(id):
    db.session.delete(WorkSchedule.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('owner_app.getWorkSchedules'))


@owner_app.route('/ownerModule/editWorkSchedule/<id>', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
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
@required_roles('admin')
@login_required
def addWorker():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, user_type='client')
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('The new employee has been added!')
        return redirect(url_for('owner_app.getWorkers'))
    return render_template('/owner/addWorkerView.html', title='Register', form=form)


@owner_app.route('/ownerModule/deleteWorker/<id>')
@required_roles('admin')
@login_required
def deleteWorker(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('owner_app.getWorkers'))
