from . import db


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')

#     def __repr__(self):
#         return '<Role %r>' % self.name


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#     # borrows = db.relationship('Borrow', backref='user', lazy='dynamic')

#     def __repr__(self):
#         return '<User %r>' % self.username


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(64), nullable=False)
    strony = db.Column(db.Integer, default=0)
    # borrows = db.relationship('Borrow', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Task %r>' % self.nazwa


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(64), nullable=False)
    opis = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.nazwa


class Graphic(db.Model):
    __tablename__ = 'graphics'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(64), nullable=False)
    akcje = db.Column(db.String(64))

    def __repr__(self):
        return '<Task %r>' % self.nazwa


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(64), nullable=False)
    data = db.Column(db.String(64))

    def __repr__(self):
        return '<Task %r>' % self.nazwa


class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    ksiazka_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    # ksiazka_id = (db.Integer,db.ForeignKey('books.id'))
    # user_id = (db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Task %r>' % self.id
