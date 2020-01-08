from flask import render_template, session, redirect, url_for, current_app, flash, request
from .. import db
from ..models import Announcement, Book, Borrow, Event, User
from . import reader_app
from flask_login import login_required, current_user
from .books import test_add_some_books, test_add_other_data
from .forms import ChangePasswordForm, ChangeEmailForm, BookTable, BorrowDateForm


<<<<<<< Updated upstream

@reader_app.route("/Reader")
@login_required
=======
@reader_app.route("/reader")
>>>>>>> Stashed changes
def reader():
    return render_template('./reader/home.html', current_user=current_user)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Books")
@login_required
=======
@reader_app.route("/reader/books")
>>>>>>> Stashed changes
def books():
    #test_add_some_books()
    books_query = db.session.query(Book)
    books_table = BookTable(books_query)
    return render_template('./reader/books.html') + books_table.__html__()


<<<<<<< Updated upstream
@reader_app.route("/Reader/Borrow", methods=['GET', 'POST'])
@login_required
=======
@reader_app.route("/reader/borrow", methods=['GET', 'POST'])
>>>>>>> Stashed changes
def borrow():
    book = Book.query.filter_by(id=request.args["id"]).first()
    dateform = BorrowDateForm()
    if dateform.validate_on_submit():
        book_id = request.args["id"]
        borrow = Borrow(book_id=book_id, user_id=current_user.id,
                        start_date=dateform.start_date.data, end_date=dateform.end_date.data)
        db.session.add(borrow)
        book.quantity = book.quantity - 1
        db.session.commit()
        return render_template('./reader/borrow.html', book=book, dateform=dateform, do_alert_success=True)
    return render_template('./reader/borrow.html', book=book, dateform=dateform)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Borrows")
@login_required
=======
@reader_app.route("/reader/borrows")
>>>>>>> Stashed changes
def borrows():
    user_borrows = Borrow.query.order_by(Borrow.id).filter_by(user_id=current_user.id).all()
    borrowed_books_dictionary = {}
    for borrow in user_borrows:
        if borrow.book_id not in borrowed_books_dictionary:
            book = Book.query.filter_by(id=borrow.book_id).first()
            borrowed_books_dictionary[borrow.book_id] = book

    # return borrowed_books_dictionary[1].name
    return render_template('./reader/borrows.html', borrows=user_borrows, borrowed_books=borrowed_books_dictionary)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Events")
@login_required
=======
@reader_app.route("/reader/events")
>>>>>>> Stashed changes
def events():
    events = Event.query.order_by(Event.id).all()
    return render_template('./reader/events.html', events=events)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Announcements")
@login_required
=======
@reader_app.route("/reader/announcements")
>>>>>>> Stashed changes
def announcements():
    announcements = Announcement.query.order_by(Announcement.id).all()
    return render_template('./reader/announcements.html', announcements=announcements)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Profiles")
@login_required
=======
@reader_app.route("/reader/profiles")
>>>>>>> Stashed changes
def profiles():
    users = User.query.order_by(User.id).all()
    return render_template('./reader/profiles.html', users=users)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Profile/<int:id>")
@login_required
=======
@reader_app.route("/reader/profile/<int:id>")
>>>>>>> Stashed changes
def profile(id):
    user = User.query.filter_by(id=id).first()
    user_borrows = Borrow.query.order_by(Borrow.id).filter_by(user_id=user.id).all()
    borrowed_books_dictionary = {}
    for borrow in user_borrows:
        if borrow.book_id not in borrowed_books_dictionary:
            book = Book.query.filter_by(id=borrow.book_id).first()
            borrowed_books_dictionary[borrow.book_id] = book
    return render_template('./reader/profile.html', borrows=user_borrows,
                           borrowed_books=borrowed_books_dictionary, user=user)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Edit")
@login_required
=======
@reader_app.route("/reader/edit")
>>>>>>> Stashed changes
def edit():
    return render_template('./reader/edit.html')


<<<<<<< Updated upstream
@reader_app.route("/Reader/Edit/Password", methods=['GET', 'POST'])
@login_required
=======
@reader_app.route("/reader/edit/password", methods=['GET', 'POST'])
>>>>>>> Stashed changes
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            # current_user.password_hash = form.password.data
            current_user.set_password(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect("/Reader/Edit/Password")
        else:
            flash('Invalid password.')
    return render_template("reader/change_password.html", form=form)


<<<<<<< Updated upstream
@reader_app.route("/Reader/Edit/Email", methods=['GET', 'POST'])
@login_required
=======
@reader_app.route("/reader/edit/email", methods=['GET', 'POST'])
>>>>>>> Stashed changes
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your Email has been updated.')
        return redirect("/reader/edit/email")
    else:
        flash('Invalid Email.')
    return render_template("/reader/change_email.html", form=form)



# @reader_app.route("/Reader/Fill")
# @login_required
# def fill():
#     test_add_some_books()
#     test_add_other_data()
#     return redirect("/Reader")




