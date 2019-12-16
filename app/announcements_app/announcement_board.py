from flask import render_template, session, redirect, url_for, request
from flask_login import login_required
from .. import db
from ..models import Announcement
from . import announcements_app
from datetime import date

@announcements_app.route('/announcement_board')
@login_required
def home():
    return render_template("announcement_board/reader_or_worker.html")


@announcements_app.route('/announcement_board/reader')
@login_required
def reader():
    return render_template("announcement_board/reader.html")


@announcements_app.route('/announcement_board/worker')
@login_required
def worker():
    return render_template("announcement_board/worker.html")


@announcements_app.route('/announcement_board/worker/add_announcement', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        announcement = Announcement(id=request.form['id'], title=request.form['title'], description=request.form['description'],
                                    date=date.today(), readerVisibility='readerVisibility' in request.form)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('announcements_app.worker'))
    return render_template('announcement_board/add_announcement.html',)


@announcements_app.route('/announcement_board/worker/get_announcements')
@login_required
def get_announcements():
    return render_template('announcement_board/get_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcement_board/worker/get_all_announcements')
@login_required
def get_all_announcements():
    return render_template('announcement_board/get_all_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcement_board/worker/get_announcement/<id>')
@login_required
def get_announcement(id):
    return render_template('announcement_board/announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )


@announcements_app.route('/announcement_board/worker/edit_announcement/<id>',  methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    if request.method == 'POST':
        announcement = Announcement.query.get_or_404(id)
        announcement.id = request.form['id']
        announcement.title = request.form['title']
        announcement.description = request.form['description']
        announcement.date = date.today()
        announcement.readerVisibility = 'readerVisibility' in request.form
        db.session.commit()
        return redirect(url_for('announcements_app.worker'))
    return render_template('announcement_board/edit_announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )


@announcements_app.route('/announcement_board/reader/get_all_reader_announcements')
@login_required
def get_all_reader_announcements():
    return render_template('announcement_board/get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(
                               Announcement.id.desc()).all()
                           )


@announcements_app.route('/announcement_board/worker/delete-announcement/<id>')
@login_required
def delete_announcement(id):
    db.session.delete(Announcement.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('announcements_app.get_all_announcements'))


@announcements_app.route('/announcement_board/worker/update-announcement/<id>')
@login_required
def update_announcement(id, Data):
    announcemt = Announcement.query.get_or_404(id)
    print(announcemt.data)
    print(Data)

    db.session.commit()
    return redirect(url_for('announcements_app.get_announcement/<id>'))
