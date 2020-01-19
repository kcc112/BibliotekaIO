from flask import render_template, request, redirect, flash
from flask_login import login_required
from .. import db
from datetime import date
from ..models import Book, Borrow, User
from . import employee_app


@employee_app.route('/employee')
def employee():
    return render_template('./employee/base.html')


@employee_app.route('/employee/books', methods=['POST', 'GET'])
# @login_required
def getBooks():
     books = Book.query.order_by(Book.id).all()
     return render_template('./employee/books.html', books=books)


@employee_app.route('/employee/books/add', methods=['POST', 'GET'])
# @login_required
def addBook():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        author = request.form['author']
        year = request.form['year']
        if name != "" and not name.isspace() and author != "" and not author.isspace() and quantity.isdigit() and year.isdigit():
            book = Book.query.filter_by(name=name).first()
            if book:
                book.quantity = book.quantity + int(quantity)
                new_book = book
            else:
                new_book = Book(name=name, quantity=quantity, author=author, year=year)
            try:
                db.session.add(new_book)
                db.session.commit()
            except:
                return 'Problems with add book'
        else:
            flash('Invalid data!')
            return redirect('/employee/books/add')
        return redirect('/employee/books')
    else:
        return render_template('employee/add.html')

@employee_app.route('/employee/books/delete/<int:id>')
# @login_required
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/employee/books')
    except:
        return 'Error occurred while removing book'


@employee_app.route('/employee/books/update/<int:id>', methods=['POST', 'GET'])
# @login_required
def updateBook(id):
    book_to_update = Book.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        author = request.form['author']
        year = request.form['year']
        if name != "" and not name.isspace() and quantity.isdigit() and author != "" and not author.isspace() and year.isdigit():
            book_to_update.name = name
            book_to_update.quantity = quantity
            book_to_update.author = author
            book_to_update.year = year

            try:
                db.session.commit()
            except:
                return 'Failed update book'
        else:
            flash('Invalid data!')
            return redirect('/employee/books/update/' + str(id))
        return redirect('/employee/books')
    else:
        return render_template('./employee/update.html', book=book_to_update)


@employee_app.route('/employee/clients')
# @login_required
def clients():
    clients = User.query.filter_by(user_type='client').all()
    return render_template('employee/clients.html', clients=clients)


@employee_app.route('/employee/clients/<int:id>')
# @login_required
def clientsBorrows(id):
    borrows = Borrow.query.filter_by(user_id=id).all()
    borrowed_books_dictionary = {}
    for borrow in borrows:
        if borrow.book_id not in borrowed_books_dictionary:
            book = Book.query.filter_by(id=borrow.book_id).first()
            borrowed_books_dictionary[borrow.book_id] = book

    return render_template('./employee/borrows.html', borrows=borrows, borrowed_books=borrowed_books_dictionary)


@employee_app.route('/employee/clients/delete/<int:id>')
# @login_required
def clientsDelete(id):
    client_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(client_to_delete)
        db.session.commit()
        return redirect('/employee/clients')
    except:
        return 'Error while removing'


@employee_app.route('/employee/borrow/ending/<int:id>')
# @login_required
def borrowEnding(id):
        borrow_to_end = Borrow.query.get_or_404(id)
        borrow_to_end.end_date = date.today()
        try:
            db.session.commit()
            return redirect('/employee/clients/' + str(borrow_to_end.user_id))
        except:
            return 'Error in ending'


@employee_app.route('/borrows')
@login_required
def borrow():
    borrow = Borrow.query.order_by(Borrow.id).all()
    return render_template('/employee/borrow_stare.html', borrows=borrow)


@employee_app.route('/borrows/delete/<int:id>')
@login_required
def deleteBorrow(id):
    borrow_to_delete = Borrow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect('/borrows')
    except:
        return 'Error while removing'
