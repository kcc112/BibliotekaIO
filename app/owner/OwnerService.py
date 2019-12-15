from flask import render_template, session, redirect, url_for, current_app, request
from app import db
from app.models import User
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