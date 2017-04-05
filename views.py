from __init__ import app, db
from models import Player
from flask import render_template, flash, redirect, session, url_for
from flask import request, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm

# index & home page routing
@app.route('/')
@app.route('/index')
def index():
    player = ('Simes')
    return render_template('index.html', title='Home', player=player)

# load a user from the db
@lm.user_loader
def load_user(playerid):
    return Player.query.get(int(playerid))

# login form view
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        player_id = Player.get_id(Player.query.filter_by(email=form.username.data))
        login_user(player_id)
        return redirect(url_for('index'))
    return render_template('login.html',
                            title='Login',
                            form=form,)

# round entry form
@app.route('/enter_round')
def enter_round():
    player = ('Adam Simon')
    return render_template('enter_round.html',
                            title='Enter Round',
                            player=player)
