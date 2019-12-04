from flask import render_template, request, redirect, flash
from .. import db
from ..models import  Book, Announcement, Event, Graphic, Borow
from . import example_app

@example_app.route("/Employee")
def employee():
    return render_template("/books/employee.html")

@example_app.route('/Books', methods=['POST','GET'])
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
                return "Problem z dodaniem ksiazki"
        else:
            flash('Blad dodania ksiazki(nazwa nie moze byc pusta)')
        return redirect("/Books")
    else:
        ksiazki = Book.query.order_by(Book.id).all()
        return render_template("/books/books.html",ksiazki=ksiazki)

@example_app.route("/Books/delete/<int:id>")
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect("/Books")
    except:
        return "Blad przy usuwaniu ksiazki"

@example_app.route("/Books/update/<int:id>",methods=['POST','GET'])
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
                return "Blad aktualizacji ksiazki"
        else:
            flash('Blad aktualizacji ksiazki(nazwa nie moze byc pusta, a strony musza byc liczba)')
        return redirect("/Books")
    else:
        return render_template('/books/update.html',ksiazka=book_to_update)

@example_app.route("/Announcements", methods=['POST','GET'])
def announcement():

    if request.method == 'POST':
        nazwa = request.form['nazwa']
        if nazwa.isspace() or nazwa == "":
            flash('Nazwa nie moze byc pusta')
            return redirect("/Announcements")
        else:
            new_announcement = Announcement(nazwa=request.form['nazwa'],opis=request.form['opis'])
            try:
                db.session.add(new_announcement)
                db.session.commit()
                return redirect("/Announcements")
            except:
                return "Problem z dodaniem ogloszenia"
    else:
        announcement = Announcement.query.order_by(Announcement.id).all()
        return render_template("/books/announcement.html",announcements=announcement)

@example_app.route("/Graphics")
def graphic():
    graphic = Graphic.query.order_by(Graphic.id).all()
    return render_template("/books/graphic.html", graphics=graphic)

@example_app.route("/Events")
def event():
    event = Event.query.order_by(Event.id).all()
    return render_template("/books/event.html", events=event)

@example_app.route("/Borrows")
def borrow():
    borrow = Borow.query.order_by(Borow.id).all()
    return render_template("/books/borrow.html", borrows=borrow)

@example_app.route("/Borrows/delete/<int:id>")
def deleteBorow(id):
    borrow_to_delete = Borow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect("/Borows")
    except:
        return "Blad przy usuwaniu wypozyczenia"

