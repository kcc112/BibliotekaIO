from . import db

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    pages = db.Column(db.Integer, default=0)
    # borrows = db.relationship('Borrow', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Task %r>' % self.name


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    readerVisibility = db.Column(db.Boolean)

    def __repr__(self):
        return '<Announcement %r>' % self.title


class Graphic(db.Model):
    __tablename__ = 'graphics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    action = db.Column(db.String(64))

    def __repr__(self):
        return '<Task %r>' % self.name


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64))

    def __repr__(self):
        return '<Task %r>' % self.nazwa



class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    # ksiazka_id = (db.Integer,db.ForeignKey('books.id'))
    # user_id = (db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Task %r>' % self.id
