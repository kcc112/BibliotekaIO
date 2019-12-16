from .. import db
from ..models import Book
from books import add_book_to_db

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