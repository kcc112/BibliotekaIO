from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Announcement, Book, Borrow, Event, User
from . import example_app
from .forms import NameForm
from .books import test_add_some_books, test_add_other_data

@example_app.route("/Reader")
def reader():
    return render_template('./reader/reader_base.html')

@example_app.route("/Reader/Borrows")
def borrows():
    borrows = Borrow.query.order_by(Borrow.id).all()
    return render_template('./reader/borrows.html', borrows=borrows)

@example_app.route("/Reader/Events")
def events():
    events = Event.query.order_by(Event.id).all()
    return render_template('./reader/events.html', events=events)

@example_app.route("/Reader/Announcements")
def announcements():
    announcements = Announcement.query.order_by(Announcement.id).all()
    return render_template('./reader/announcements.html', announcements=announcements)

@example_app.route("/Reader/Profiles")
def profiles():
    users = User.query.order_by(User.id).all()
    return render_template('./reader/profiles.html', users=users)

@example_app.route("/Reader/Edit")
def edit():
    return render_template('./reader/edit.html')

@example_app.route("/Reader/Fill")
def fill():
    test_add_some_books()
    test_add_other_data()
    return redirect("/Reader")




