from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    password = PasswordField('password', validators=[DataRequired()])

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
