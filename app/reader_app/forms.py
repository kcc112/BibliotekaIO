from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask_table import Table, Col, ButtonCol
from ..models import User
from wtforms.fields.html5 import DateField
from datetime import date
from datetime import timedelta


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BookTable(Table):
    classes = ['table']
    name = Col('Name')
    author = Col('Author')
    quantity = Col('Quantity')
    year = Col('Year')
    borrow = ButtonCol('Borrow', 'reader_app.borrow', url_kwargs=dict(
        id='id'), button_attrs={'class': 'btn btn-primary btn-sm'})


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
                             DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')


class BorrowDateForm(FlaskForm):
    #dt = DateField('DatePicker', format='%Y-%m-%d', default=date.today())
    start_date = DateField(
        'DatePicker', format='%Y-%m-%d', default=date.today())
    end_date = DateField('DatePicker', format='%Y-%m-%d',
                         default=date.today() + timedelta(days=7))
    submit = SubmitField('Submit', validators=[DataRequired()])

class BookSearchForm(FlaskForm):
    title_search = StringField('')
    author_search = StringField('')
    submit = SubmitField('Search', validators=[DataRequired()])
