from flask import render_template, request, redirect, flash
from .. import db
from ..models import Book, Announcement, Event, Graphic, Borrow
from . import books_app


@books_app.route('/employee')
def employee():
    return render_template('/books/employee.html')


@books_app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        strony = request.form['strony']
        if nazwa != "" and not nazwa.isspace():
            if strony.isdigit():
                nowa_ksiazka = Book(nazwa=nazwa, strony=strony)
            else:
                nowa_ksiazka = Book(nazwa=nazwa)
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
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/books')
    except:
        return 'blad przy usuwaniu ksiazki'


@books_app.route('/books/update/<int:id>', methods=['POST', 'GET'])
def updateBook(id):
    book_to_update = Book.query.get_or_404(id)

    if request.method == 'POST':
        nazwa = request.form['nazwa']
        strony = request.form['strony']
        if nazwa != "" and not nazwa.isspace() and strony.isdigit():
            book_to_update.nazwa = nazwa
            book_to_update.strony = strony

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


@books_app.route('/announcements', methods=['POST', 'GET'])
def announcement():

    if request.method == 'POST':
        nazwa = request.form['nazwa']
        if nazwa.isspace() or nazwa == "":
            flash('Nazwa nie moze byc pusta')
            return redirect('/announcements')
        else:
            new_announcement = Announcement(
                nazwa=request.form['nazwa'], opis=request.form['opis'])
            try:
                db.session.add(new_announcement)
                db.session.commit()
                return redirect('/announcements')
            except:
                return 'Problem z dodaniem ogloszenia'
    else:
        announcement = Announcement.query.order_by(Announcement.id).all()
        return render_template('/books/announcement.html', announcements=announcement)


@books_app.route('/graphics')
def graphic():
    graphic = Graphic.query.order_by(Graphic.id).all()
    return render_template('/books/graphic.html', graphics=graphic)


@books_app.route('/events')
def event():
    event = Event.query.order_by(Event.id).all()
    # b = Event(id=2, nazwa="nazwa", data='data')
    # db.session.add(b)
    # db.session.commit()
    return render_template("/books/event.html", events=event)


@books_app.route('/borrows')
def borrow():
    borrow = Borrow.query.order_by(Borrow.id).all()
    return render_template("/books/borrow.html", borrows=borrow)


@books_app.route('/borrows/delete/<int:id>')
def deleteBorrow(id):
    borrow_to_delete = Borrow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect('/borrows')
    except:
        return 'Blad przy usuwaniu wypozyczenia'
