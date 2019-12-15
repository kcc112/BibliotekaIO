from flask import render_template, session, redirect, url_for, current_app, request
from app import db
from app.models import User, WorkSchedule
from app.owner import owner
from datetime import date


@owner.route('/ownerModule/ownerView')
def ownerView():
    return render_template('owner/ownerView.html')


@owner.route('/ownerModule/getWorkers')
def getWorkers():
    return render_template('owner/getWorkersView.html',
                           users=User.query.order_by(User.id.desc()).all()
                           )


@owner.route('/ownerModule/getWorkSchedules')
def getWorkSchedules():
    return render_template('owner/workSchedules.html',
                           workSchedules=WorkSchedule.query.order_by(WorkSchedule.id.desc()).all()
                           )


@owner.route('/ownerModule/addWorker', methods=['GET', 'POST'])
def addWorker():
    if request.method == 'POST':
        user = User(id=request.form['id'], username=request.form['username'],
                    role_id=request.form['role_id'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('getWorkers'))
    return render_template('owner/addWorkerView.html')


@owner.route('/ownerModule/deleteWorker/<id>')
def delete_event(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('getWorkers'))


@owner.route('/ownerModule/getWorker/<id>')
def get_event(id):
    return render_template('event.html',
                           user=User.query.get_or_404(id)
                           )
