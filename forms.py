from flask_wtf import Form
from wtforms import (StringField, BooleanField, PasswordField, DateField,
                    IntegerField)
from wtforms.fields.html5 import TelField
from wtforms.validators import (DataRequired, Email, ValidationError, Regexp,
                                Length, EqualTo)


from models import Player

def name_exists(form, field):
    if Player.select().where(Player.username == field.data).exists():
        raise ValidationError('Player with this name already exists')

def email_exists(form, field):
    if Player.select().where(Player.username == field.data).exists():
        raise ValidationError('Player with this email already exists')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)

class EnterRoundForm(Form):
    dateplayed = DateField('dateplayed', validators=[DataRequired()])
    coursename = StringField('coursename', validators=[DataRequired()])
    teebox = StringField('teebox', validators=[DataRequired()])
    slope = IntegerField('slope', validators=[DataRequired()])
    rating = IntegerField('rating', validators=[DataRequired()])
    putts_front = IntegerField('putts_front', validators=[DataRequired()])
    putts_back = IntegerField('putts_back', validators=[DataRequired()])
    strokes_front = IntegerField('strokes_front', validators=[DataRequired()])
    strokes_back = IntegerField('strokes_back', validators=[DataRequired()])
    handicap = IntegerField('handicap', validators=[DataRequired()])
    quota = IntegerField('quota', validators=[DataRequired()])

class RegisterForm(Form):
    firstname = StringField('First Name',
                            validators=[DataRequired()])
    lastname = StringField('Last Name',
                            validators=[DataRequired()])
    nickname = StringField('Nickname',
                            validators=[DataRequired(),
                            Regexp(
                                r'^[a-zA-Z0-9]+$',
                                message=('username should be one word, with '
                                'only letters and numbers...nooch')),
                                name_exists
                                ])
    cellphone = TelField('Cellphone')
    email = StringField('Email',
                        validators=[DataRequired(),
                        Email(),
                        email_exists])
    password = PasswordField('Password',
                            validators=[DataRequired(),
                                        Length(min=2),
                                        EqualTo('password2',
                                                message='Passwords must match')])
    password2 = PasswordField('Confirm Password',
                            validators=[DataRequired()])

class CliaForm(Form):
    fac_name = StringField('Facility Name',
                            validators=[DataRequired()])
    fac_street_address = StringField('Facility Street Address')
    fac_city = StringField('Facility City')
    fac_state = StringField('Facility State')
    fac_zip = StringField('Facility Zip')
