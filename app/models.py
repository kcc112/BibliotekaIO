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


class WorkSchedule(db.Model):
    __tablename__ = 'work_schedules'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(64))
    startTime = db.Column(db.Time())
    endTime = db.Column(db.Time())
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<WorkSchedule %r>' % self.id
