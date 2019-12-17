from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_table import Table, Col, ButtonCol
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
    borrow = ButtonCol('Borrow', 'example_app.borrow', url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-primary btn-sm'})

class BorrowDateForm(FlaskForm):
    #dt = DateField('DatePicker', format='%Y-%m-%d', default=date.today())
    start_date = DateField('DatePicker', format='%Y-%m-%d', default=date.today())
    end_date = DateField('DatePicker', format='%Y-%m-%d', default=date.today() + timedelta(days=7))
    submit = SubmitField('Submit', validators=[DataRequired()])