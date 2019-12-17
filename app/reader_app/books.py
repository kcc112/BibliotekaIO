from datetime import date
from .. import db
from ..models import Announcement, Book, Borrow, Event, User

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

    # b1 = Book(name="Name1", pages="100")
    # b2 = Book(name="Name2", pages="200")
    # b3 = Book(name="Name3", pages="300")
    # b4 = Book(name="Name4", pages="400")
    # b5 = Book(name="Name5", pages="500")

    add_book_to_db(b1)
    add_book_to_db(b2)
    add_book_to_db(b3)
    add_book_to_db(b4)
    add_book_to_db(b5)

def test_add_other_data():
    new_announcement1 = Announcement(title="Ogłoszenie1", description="Opis1", date=date(2002, 12, 31))
    new_announcement2 = Announcement(title="Ogłoszenie2", description="Opis2", date=date(2002, 12, 31))
    new_announcement3 = Announcement(title="Ogłoszenie3", description="Opis3", date=date(2002, 12, 31))
    db.session.add(new_announcement1)
    db.session.add(new_announcement2)
    db.session.add(new_announcement3)
    new_event1 = Event(name="Wydarzenie1", date="data1")
    new_event2 = Event(name="Wydarzenie2", date="data2")
    new_event3 = Event(name="Wydarzenie3", date="data3")
    db.session.add(new_event1)
    db.session.add(new_event2)
    db.session.add(new_event3)
    new_user1 = User()
    db.session.add(new_user1)
    db.session.commit()

