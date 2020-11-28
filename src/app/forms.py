from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired


class EnterExisting(FlaskForm):
    hat_number = StringField('Hat Number', validators=[InputRequired('Hat number is required')])

    submit = SubmitField('Draw')


class AddName(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name is required')])

    submit = SubmitField('Add')


class CreateNew(FlaskForm):
    name1 = StringField('name1', validators=[InputRequired('At least 1 name is required')])
    name2 = StringField('name2')

    submit = SubmitField('Login')
