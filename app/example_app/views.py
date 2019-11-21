from flask import render_template, request, session, redirect, url_for, current_app
from .. import db
from ..models import User, Book, Announcement, Event, Graphic, Borow
from . import example_app
from .forms import NameForm


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

@example_app.route('/Books', methods=['POST','GET'])
def books():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        strony = request.form['strony']
        nowa_ksiazka = Book(nazwa=nazwa, strony=strony)

        try:
            db.session.add(nowa_ksiazka)
            db.session.commit()
            return redirect("/Books")
        except:
            return "Problem z dodaniem ksiazki"
    else:
        ksiazki = Book.query.order_by(Book.id).all()
        return render_template("/example_app/books.html",ksiazki=ksiazki)

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
        if request.form['nazwa'] != "":
            book_to_update.nazwa = request.form['nazwa']
            book_to_update.strony = request.form['strony']

            try:
                db.session.commit()
            except:
                return "Blad aktualizacji ksiazki"
        return redirect("/Books")
    else:
        return render_template('/example_app/update.html',ksiazka=book_to_update)

@example_app.route("/Announcements", methods=['POST','GET'])
def announcement():

    if request.method == 'POST':
        new_announcement = Announcement(nazwa=request.form['nazwa'],opis=request.form['opis'])
        try:
            db.session.add(new_announcement)
            db.session.commit()
            return redirect("/Announcements")
        except:
            return "Problem z dodaniem ogloszenia"
    else:
        announcement = Announcement.query.order_by(Announcement.id).all()
        return render_template("/example_app/announcement.html",announcements=announcement)

@example_app.route("/Graphics")
def graphic():
    graphic = Graphic.query.order_by(Graphic.id).all()
    return render_template("/example_app/graphic.html", graphics=graphic)

@example_app.route("/Events")
def event():
    event = Event.query.order_by(Event.id).all()
    return render_template("/example_app/event.html", events=event)

@example_app.route("/Borrows")
def borrow():
    borrow = Borow.query.order_by(Borow.id).all()
    return render_template("/example_app/borrow.html", borrows=borrow)

@example_app.route("/Borrows/delete/<int:id>")
def deleteBorow(id):
    borrow_to_delete = Borow.query.get_or_404(id)

    try:
        db.session.delete(borrow_to_delete)
        db.session.commit()
        return redirect("/Borows")
    except:
        return "Blad przy usuwaniu wypozyczenia"

