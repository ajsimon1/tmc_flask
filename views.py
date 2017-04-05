from __init__ import app
from flask import render_template, flash, redirect, url_for
from forms import LoginForm, EnterRoundForm

# index & home page routing
@app.route('/')
@app.route('/index')
def index():
    player = ('Simes')
    return render_template('index.html', title='Home', player=player)

# login form view
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.username.data, str(form.remember_me.data)))
        return redirect(url_for('index'))
    return render_template('login.html',
                            title='Login',
                            form=form,)

# round entry form
@app.route('/enter_round', methods=['GET', 'POST'])
def enter_round():
    player = ('Adam Simon')
    form = EnterRoundForm()
    if form.validate_on_submit():
        round = Round(playerid = 1,
                    courseid = 1,
                    dateplayed = form.dateplayed.data,
                    slope = form.slope.data,
                    rating = form.slope.rating,
                    strokes_front = form.strokes_front.data,
                    strokes_back = form.strokes_back.data,
                    strokes_total = int(form.strokes_front.data) + int(form.strokes_back.data),
                    putts_front = form.putts_front.data,
                    putts_back = form.putts_back.data,
                    putts_total = int(form.putts_front.data) + int(putts_back.form.data),
                    strokes_front = form.strokes_front.data
                    )
        flash("You're round at {coursename} on {dateplayed} has been submitted to the GateKeeper").format(
            form.coursename.date, form.dateplayed.data)
        return render_template('enter_round.html')
    return render_template('enter_round.html',
                            title='Enter Round',
                            player=player,
                            form=form)
