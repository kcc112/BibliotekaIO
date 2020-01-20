from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required
from .. import db
from ..models import User, WorkSchedule
from . import owner_app
from ..registration_login_app import forms
from app.registration_login_app.registration_login import required_roles
import datetime


@owner_app.route('/owner')
@required_roles('admin')
@login_required
def owner():
    return render_template('/owner/owner.html')


@owner_app.route('/owner/workers')
@required_roles('admin')
@login_required
def workers():
    return render_template('owner/workers.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/owner/work_schedules')
@required_roles('admin', 'employee')
@login_required
def schedules():
    return render_template('/owner/schedules.html', workSchedules=WorkSchedule.query.order_by(WorkSchedule.id.desc()).all())


@owner_app.route('/owner/add/schedule', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def add_schedule():
    if request.method == 'POST':
        work_schedule = WorkSchedule(day=request.form['day'],startTime=datetime.time(int(request.form['start_time'].split(":")[0]), int(request.form['start_time'].split(":")[1])),endTime=datetime.time(int(request.form['end_time'].split(":")[0]), int(request.form['end_time'].split(":")[1])),worker_id=request.form['worker_id'])

        db.session.add(work_schedule)
        db.session.commit()
        return redirect(url_for('owner_app.schedules'))
    return render_template('owner/add_schedule.html', users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/owner/delete/schedule/<id>')
@required_roles('admin')
@login_required
def delete_schedule(id):
    db.session.delete(WorkSchedule.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('owner_app.schedules'))


@owner_app.route('/owner/edit/schedule/<id>', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def edit_schedule(id):
    work_schedule = WorkSchedule.query.get(id)
    if request.method == 'POST':
        work_schedule.day = request.form['day']
        work_schedule.startTime = datetime.time(int(request.form['start_time'].split(":")[0]), int(request.form['start_time'].split(":")[1]))
        work_schedule.endTime = datetime.time(int(request.form['end_time'].split(":")[0]), int(request.form['end_time'].split(":")[1]))
        work_schedule.worker_id = request.form['worker_id']
        db.session.commit()
        return redirect(url_for('owner_app.schedules'))
    return render_template('owner/edit_schedule.html', workSchedule=work_schedule, users=User.query.order_by(User.id.desc()).all())


@owner_app.route('/owner/add/worker', methods=['GET', 'POST'])
@required_roles('admin')
@login_required
def add_worker():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, user_type='client')
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('The new employee has been added!')
        return redirect(url_for('owner_app.workers'))
    return render_template('/owner/add_worker.html', title='Register', form=form)


@owner_app.route('/owner/delete/worker/<id>')
@required_roles('admin')
@login_required
def delete_worker(id):
    user = User.query.get_or_404(id)
    if user.user_type != "admin":
        db.session.delete(user)
        db.session.commit()
    else:
        flash('Can\'t delete this user', 'error')

    return redirect(url_for('owner_app.workers'))
