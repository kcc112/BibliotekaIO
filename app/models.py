from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Auditorium(db.Model):
    __tablename__ = 'auditorium'
    id = db.Column(db.Integer, primary_key=True)
    maxPlaces = db.Column(db.Integer)
    number = db.Column(db.Integer)

    def __repr__(self):
        return '<Auditorium %r>' % self.number


# klasa laczaca user z event ( bo jest to relacja many-to-many) - nazwe lepsza trzeba wybrac
tags = db.Table('tags',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                )


#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(80), nullable=False)
#    surname = db.Column(db.String(80), nullable=False)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # nwm jak tutaj wiele uzytkownikow zrobic
    # users = db.relationship("User", backref = "event")
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    # time = db.Column(db.Time)
    auditorium = db.Column(db.Integer, db.ForeignKey('auditorium.id'))
    # tags = db.relationship('User', secondary=tags, lazy='subquery',
    #                        backref=db.backref('event', lazy=True))

    def __init__(self, id, name, description, date, auditorium):#, auditorium, tags):
        self.id = id
        self.name = name
        self.description = description
        self.date = date
        self.auditorium = auditorium
        # self.auditorium = auditorium
        # self.tags = tags

    def __repr__(self):
        return '<Event %r>' % self.name