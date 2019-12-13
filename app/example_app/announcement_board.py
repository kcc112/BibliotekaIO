from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..models import Announcement
from . import example_app
from .forms import NameForm
from datetime import date

@example_app.route('/announcement_board')
def home():
    return render_template("announcement_board/readerOrWorker.html")

@example_app.route('/announcement_board/reader')
def reader():
    return render_template("announcement_board/reader.html")

@example_app.route('/announcement_board/worker')
def worker():
    return render_template("announcement_board/worker.html")


@example_app.route('/announcement_board/worker/add_announcement', methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        announcement = Announcement(id=request.form['id'], title=request.form['title'], description=request.form['description'],
                                    date=date.today(),readerVisibility='readerVisibility' in request.form)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('worker'))
    return render_template('announcement_board/add_announcement.html',)

@example_app.route('/announcement_board/worker/get_announcements')
def get_announcements():
    return render_template('announcement_board/get_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@example_app.route('/announcement_board/worker/get_all_announcements')
def get_all_announcements():
    return render_template('announcement_board/get_all_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@example_app.route('/announcement_board/worker/get_announcement/<id>')
def get_announcement(id):
    return render_template('announcement_board/announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )

@example_app.route('/announcement_board/worker/edit_announcement/<id>',  methods=['GET', 'POST'])
def edit_announcement(id):
    if request.method == 'POST':
        announcement = Announcement.query.get_or_404(id)
        announcement.id = request.form['id']
        announcement.title = request.form['title']
        announcement.description = request.form['description']
        announcement.date = date.today()
        announcement.readerVisibility = 'readerVisibility' in request.form
        db.session.commit()
        return redirect(url_for('worker'))
    return render_template('announcement_board/edit_announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )

@example_app.route('/announcement_board/reader/get_all_reader_announcements')
def get_all_reader_announcements():
    return render_template('announcement_board/get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@example_app.route('/announcement_board/worker/delete-announcement/<id>')
def delete_announcement(id):
    db.session.delete(Announcement.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('announcement_board/get_all_announcements'))

@example_app.route('/announcement_board/worker/update-announcement/<id>')
def update_announcement(id,Data):
    announcemt = Announcement.query.get_or_404(id)
    print(announcemt.data)
    print(Data)

    db.session.commit()
    return redirect(url_for('announcement_board/get_announcement/<id>'))