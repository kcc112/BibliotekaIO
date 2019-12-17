from flask import render_template, request, redirect, flash
from flask_login import login_required
from .. import db
from ..models import Book, Event, Graphic, Borrow
from . import books_app


@books_app.route('/books', methods=['POST', 'GET'])
@login_required
def books():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        strony = request.form['strony']
        if nazwa != "" and not nazwa.isspace():
            if strony.isdigit():
                nowa_ksiazka = Book(name=nazwa, pages=strony)
            else:
                nowa_ksiazka = Book(name=nazwa)
            try:
                db.session.add(nowa_ksiazka)
                db.session.commit()
            except:
                return 'Problem z dodaniem ksiazki'
        else:
            flash('Blad dodania ksiazki(nazwa nie moze byc pusta)')
        return redirect('/books')
    else:
        ksiazki = Book.query.order_by(Book.id).all()
        return render_template('/books/books.html', ksiazki=ksiazki)


@books_app.route('/books/delete/<int:id>')
@login_required
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/books')
    except:
        return 'blad przy usuwaniu ksiazki'


@books_app.route('/books/update/<int:id>', methods=['POST', 'GET'])
@login_required
def updateBook(id):
    book_to_update = Book.query.get_or_404(id)

    if request.method == 'POST':
        nazwa = request.form['nazwa']
        strony = request.form['strony']
        if nazwa != "" and not nazwa.isspace() and strony.isdigit():
            book_to_update.name = nazwa
            book_to_update.pages = strony

            try:
                db.session.commit()
            except:
                return 'Blad aktualizacji ksiazki'
        else:
            flash(
                'Blad aktualizacji ksiazki(nazwa nie moze byc pusta, a strony musza byc liczba)')
        return redirect('/books')
    else:
        return render_template('/books/update.html', ksiazka=book_to_update)


@books_app.route('/graphics')
@login_required
def graphic():
    graphic = Graphic.query.order_by(Graphic.id).all()
    return render_template('/books/graphic.html', graphics=graphic)


@books_app.route('/events')
@login_required
def event():
    event = Event.query.order_by(Event.id).all()
    # b = Event(id=2, nazwa="nazwa", data='data')
    # db.session.add(b)
    # db.session.commit()
    return render_template("/books/event.html", events=event)


@books_app.route('/borrows')
@login_required
def borrow():
    borrow = Borrow.query.order_by(Borrow.id).all()
    return render_template("/books/borrow.html", borrows=borrow)


@books_app.route('/borrows/delete/<int:id>')
@login_required
def deleteBorrow(id):
    borrow_to_delete = Borrow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect('/borrows')
    except:
        return 'Blad przy usuwaniu wypozyczenia'
