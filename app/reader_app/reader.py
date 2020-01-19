from flask import render_template, session, redirect, flash, request, url_for
from .. import db
from ..models import Announcement, Book, Borrow, Event, User
from . import reader_app
from flask_login import login_required, current_user
from app.registration_login_app.registration_login import required_roles
from .forms import ChangePasswordForm, ChangeEmailForm, BookTable, BorrowDateForm


@reader_app.route('/reader')
@login_required
@required_roles('client')
def reader():
    return render_template('./reader/home.html', current_user=current_user)


@reader_app.route('/reader/books')
@login_required
@required_roles('client')
def books():
    books_query = db.session.query(Book)
    books_table = BookTable(books_query)
    return render_template('./reader/books.html') + books_table.__html__()


@reader_app.route('/reader/borrow', methods=['GET', 'POST'])
@login_required
@required_roles('client')
def borrow():
    book = Book.query.filter_by(id=request.args['id']).first()
    dateform = BorrowDateForm()
    if dateform.validate_on_submit():
        book_id = request.args['id']
        borrow = Borrow(book_id=book_id, user_id=current_user.id,
                        start_date=dateform.start_date.data, end_date=dateform.end_date.data)
        db.session.add(borrow)
        book.quantity = book.quantity - 1
        db.session.commit()
        return render_template('./reader/borrow.html', book=book, dateform=dateform, do_alert_success=True)
    return render_template('./reader/borrow.html', book=book, dateform=dateform)


@reader_app.route('/reader/borrows')
@login_required
@required_roles('client')
def borrows():
    user_borrows = Borrow.query.order_by(
        Borrow.id).filter_by(user_id=current_user.id).all()
    borrowed_books_dictionary = {}
    for borrow in user_borrows:
        if borrow.book_id not in borrowed_books_dictionary:
            book = Book.query.filter_by(id=borrow.book_id).first()
            borrowed_books_dictionary[borrow.book_id] = book

    return render_template('./reader/borrows.html', borrows=user_borrows, borrowed_books=borrowed_books_dictionary)


@reader_app.route('/reader/events')
@login_required
@required_roles('client')
def events():
    events = Event.query.order_by(Event.id).all()
    return render_template('./reader/events.html', events=events)


@reader_app.route('/reader/event/<int:id>')
@login_required
@required_roles('client')
def event(id):
    event = Event.query.filter_by(id=id).first()
    return render_template('./reader/event.html', event=event)


@reader_app.route('/reader/announcements')
@login_required
@required_roles('client')
def announcements():
    announcements = Announcement.query.order_by(Announcement.id).all()
    return render_template('./reader/announcements.html', announcements=announcements)


@reader_app.route('/reader/announcement/<int:id>')
@login_required
@required_roles('client')
def announcement(id):
    announcement = Announcement.query.filter_by(id=id).first()
    return render_template('./reader/announcement.html', announcement=announcement)


@reader_app.route('/reader/profiles')
@login_required
@required_roles('client')
def profiles():
    users = User.query.order_by(User.id).all()
    return render_template('./reader/profiles.html', users=users)


@reader_app.route('/reader/profile/<int:id>')
@login_required
@required_roles('client')
def profile(id):
    user = User.query.filter_by(id=id).first()
    user_borrows = Borrow.query.order_by(
        Borrow.id).filter_by(user_id=user.id).all()
    borrowed_books_dictionary = {}
    for borrow in user_borrows:
        if borrow.book_id not in borrowed_books_dictionary:
            book = Book.query.filter_by(id=borrow.book_id).first()
            borrowed_books_dictionary[borrow.book_id] = book
    return render_template('./reader/profile.html', borrows=user_borrows,
                           borrowed_books=borrowed_books_dictionary, user=user)


@reader_app.route('/reader/edit')
@login_required
@required_roles('client')
def edit():
    return render_template('./reader/edit.html')


@reader_app.route('/reader/edit/password', methods=['GET', 'POST'])
@login_required
@required_roles('client')
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('reader_app.change_password'))
        else:
            flash('Invalid password.')
    return render_template('reader/change_password.html', form=form)


@reader_app.route('/reader/edit/email', methods=['GET', 'POST'])
@login_required
@required_roles('client')
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your Email has been updated.')
        return redirect(url_for('reader_app.change_email'))
    else:
        flash('Invalid Email.')
    return render_template('/reader/change_email.html', form=form)
