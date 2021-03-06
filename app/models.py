from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date
from app import login
from . import db
import enum


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    author = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer, index=True)
    year = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Task %r>' % self.name


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.String(150), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
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


class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.Date, default=date.today())
    end_date = db.Column(db.Date)

    def __repr__(self):
        return '<Task %r>' % self.id


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, user_type):
        return user_type == self.user_type


class WorkSchedule(db.Model):
    __tablename__ = 'work_schedules'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    startTime = db.Column(db.Time())
    endTime = db.Column(db.Time())
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<WorkSchedule %r>' % self.id


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Auditorium(db.Model):
    __tablename__ = 'auditorium'
    id = db.Column(db.Integer, primary_key=True)
    maxPlaces = db.Column(db.Integer)
    number = db.Column(db.Integer)

    def __repr__(self):
        return '<Auditorium %r>' % self.number


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    auditorium = db.Column(db.Integer, db.ForeignKey('auditorium.id'))

    def __repr__(self):
        return '<Event %r>' % self.name


class UserEvent(db.Model):
    __tablename__ = 'user_event'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
