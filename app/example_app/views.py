from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from . import example_app
from .forms import NameForm
from .forms import BookTable
from ..models import Book


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


@example_app.route("/Reader/Books")
def books():
    #test_add_some_books()
    books_query = db.session.query(Book)
    books_table = BookTable(books_query)
    return render_template('./reader/books.html') + books_table.__html__()      

@example_app.route("/Reader/Borrow")
def borrow():
    return render_template('./reader/borrow.html')    
