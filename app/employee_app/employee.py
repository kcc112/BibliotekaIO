from flask import render_template, request, redirect, flash
from flask_login import login_required
from .. import db
from ..models import Book, Borrow
from . import employee_app


@employee_app.route('/Employee')
def employee():
    return render_template('employee/employee.html')


@employee_app.route('/Employee/Books', methods=['POST', 'GET'])
# @login_required
def getBooks():
     books = Book.query.order_by(Book.id).all()
     return render_template('./employee/books.html', books=books)


@employee_app.route('/Employee/Books/Add', methods=['POST', 'GET'])
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
            return redirect('/Employee/Books/Add')
        return redirect('/Employee/Books')
    else:
        return render_template('employee/add.html')

@employee_app.route('/Employee/Books/Delete/<int:id>')
# @login_required
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/Employee/Books')
    except:
        return 'blad przy usuwaniu ksiazki'


@employee_app.route('/Employee/Books/Update/<int:id>', methods=['POST', 'GET'])
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
            return redirect('/Employee/Books/Update/'+str(id))
        return redirect('/Employee/Books')
    else:
        return render_template('./employee/update.html', book=book_to_update)


@employee_app.route('/borrows')
@login_required
def borrow():
    borrow = Borrow.query.order_by(Borrow.id).all()
    return render_template("/employee/borrow.html", borrows=borrow)


@employee_app.route('/borrows/delete/<int:id>')
@login_required
def deleteBorrow(id):
    borrow_to_delete = Borrow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect('/borrows')
    except:
        return 'Blad przy usuwaniu wypozyczenia'
