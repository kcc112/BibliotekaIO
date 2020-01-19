from flask import render_template, session, redirect, url_for, request
from flask_login import login_required
from flask_uuid import FlaskUUID
from .. import db
from ..models import Announcement
from . import announcements_app
from datetime import date
import uuid

@announcements_app.route('/announcements')
@login_required
def home():
    return render_template("/announcements/reader_or_employee.html")


@announcements_app.route('/announcements/reader')
@login_required
def reader():
    return render_template("/announcements/reader.html")


@announcements_app.route('/announcements/employee')
@login_required
def employee():
    return render_template("/announcements/employee.html")


@announcements_app.route('/announcements/employee/add_announcement', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        announcement = Announcement(id=str(uuid.uuid4()), title=request.form['title'], description=request.form['description'],
                                    date=date.today(), readerVisibility='readerVisibility' in request.form)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('announcements_app.employee'))
    return render_template('announcements/add_announcement.html',)


@announcements_app.route('/announcements/employee/get_announcements')
@login_required
def get_announcements():
    return render_template('announcements/get_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcements/employee/get_all_announcements')
@login_required
def get_all_announcements():
    return render_template('announcements/get_all_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcements/employee/get_announcement/<id>')
@login_required
def get_announcement(id):
    return render_template('announcements/announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )


@announcements_app.route('/announcements/employee/edit_announcement/<id>',  methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    if request.method == 'POST':
        announcement = Announcement.query.get_or_404(id)
        #announcement.id = request.form['id']
        announcement.title = request.form['title']
        announcement.description = request.form['description']
        announcement.date = date.today()
        announcement.readerVisibility = 'readerVisibility' in request.form
        db.session.commit()
        return redirect(url_for('announcements_app.employee'))
    return render_template('announcements/edit_announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )


@announcements_app.route('/announcements/reader/get_all_reader_announcements')
@login_required
def get_all_reader_announcements():
    return render_template('announcements/get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcements/employee/delete-announcement/<id>')
@login_required
def delete_announcement(id):
    db.session.delete(Announcement.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('announcements_app.get_all_announcements'))


@announcements_app.route('/announcements/employee/update-announcement/<id>')
@login_required
def update_announcement(id, Data):
    announcemt = Announcement.query.get_or_404(id)
    print(announcemt.data)
    print(Data)

    db.session.commit()
    return redirect(url_for('announcements.get_announcement/<id>'))
