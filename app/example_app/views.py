from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..models import Announcement
from . import example_app
from .forms import NameForm
from datetime import date


@example_app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('example_app/index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
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
        return redirect(url_for('announcement_board/worker'))
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
@example_app.route('/announcement_board/reader/get_all_reader_announcements')
def get_all_reader_announcements():
    return render_template('announcement_board/get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )
