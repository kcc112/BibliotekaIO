from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_table import Table, Col, ButtonCol


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