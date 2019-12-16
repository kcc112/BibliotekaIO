from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Announcement, Book, Borrow, Event, User
from . import example_app
from .forms import NameForm

def add_book_to_db(book_to_add):
    book = Book.query.filter_by(name=book_to_add.name).first()
    if book is None:
        db.session.add(book_to_add)
        db.session.commit()

def get_all_books():
    books_list = []
    books_in_db = Book.query().all()
    for book in books_in_db:
        books_list.append(book)
    return books_list

def test_add_some_books():
    b1 = Book(name="Obcy", author="Albert Camus", quantity=30, year=1942)
    b2 = Book(name="W poszukiwaniu straconego czasu ", author="Marcel Proust", quantity=15, year=1913)
    b3 = Book(name="Proces", author="Franz Kafka", quantity=22, year=1925)
    b4 = Book(name="Mały Książę", author="Antoine de Saint-Exupéry", quantity=55, year=1943)
    b5 = Book(name="Dola człowiecza", author="André Malraux", quantity=12, year=1933)

    add_book_to_db(b1)
    add_book_to_db(b2)
    add_book_to_db(b3)
    add_book_to_db(b4)
    add_book_to_db(b5)

def test_add_other_data():
    new_announcement1 = Announcement(nazwa="Ogłoszenie1", opis="Opis1")
    new_announcement2 = Announcement(nazwa="Ogłoszenie2", opis="Opis2")
    new_announcement3 = Announcement(nazwa="Ogłoszenie3", opis="Opis3")
    db.session.add(new_announcement1)
    db.session.add(new_announcement2)
    db.session.add(new_announcement3)
    new_event1 = Event(nazwa="Wydarzenie1", data="data1")
    new_event2 = Event(nazwa="Wydarzenie2", data="data2")
    new_event3 = Event(nazwa="Wydarzenie3", data="data3")
    db.session.add(new_event1)
    db.session.add(new_event2)
    db.session.add(new_event3)
    new_user1 = User()
    db.session.add(new_user1)
    db.session.commit()