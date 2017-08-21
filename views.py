from __init__ import app, db, login_manager, ALLOWED_EXTENSIONS
from flask import render_template, flash, redirect, url_for, request, Response
from flask import send_from_directory, g, session
from flask_login import login_required, current_user, logout_user, login_user
from forms import LoginForm, EnterRoundForm, RegisterForm, CliaForm
from models import Round, Player
from alexTrafficProject import exportable_json
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename

import json
import os
import requests

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(playerid):
    return Player.query.get(int(playerid))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/clia_api', methods=['POST', 'GET'])
def clia_api():
    form = CliaForm()
    if request.method == 'POST' and form.validate_on_submit:
        # flash('Pinging CLIA API, results will display below')
        clia_api_endpoint = 'https://data.cms.gov/resource/auvt-6sjc.json'
        query_string = ""
        if form.fac_name.data:
            query_string = "?$where=fac_name like'%25{}%25'".format(str(form.fac_name.data).upper())
        if form.fac_street_address.data:
            query_string += "&st_adr={}".format(form.fac_street_address.data)
        if form.fac_city.data:
            query_string += "&city_name={}".format(str(form.fac_city.data).upper())
        if form.fac_state.data:
            query_string += "&state_cd={}".format(str(form.fac_state.data).upper())
        if form.fac_zip.data:
            query_string += "&zip_cd={}".format(form.fac_zip.data)
        response = requests.get(clia_api_endpoint + query_string)
        json_resp = json.loads(response.text)
        return render_template('clia_api.html', data=json_resp, form=form, query=query_string)
    return render_template('clia_api.html', form=form)

@app.route('/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit:
        flash('You\'ve successfully registered, now login...bitch')
        player = Player(firstname = form.firstname.data,
                        lastname = form.lastname.data,
                        nickname = form.nickname.data,
                        email = form.email.data,
                        cellphone = form.cellphone.data,
                        password = sha256_crypt.encrypt(str(form.password.data)))
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# login form view
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.email.data
        user = Player.query.filter_by(email=username).first()
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                login_user(user)
                session['username'] = user.nickname
                session['logged_in'] = True
                flash('You\'ve succesfully logged in, happy DYWGRing')
                return redirect(url_for('index'))
            else:
                flash('You\'re email or password is incorrect')
                return redirect(url_for('login'))
        else:
            flash('No user found with that email, did you register dickbag?')
            return redirect(url_for('login'))
    return render_template('login.html',
                            title='Login',
                            form=form,)
# home page routing
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('You\'ve been successfully logged off, by Brian, dutch rudder style')
    return redirect(url_for('login'))

@app.route('/gallery/<filename>')
@login_required
def send_image(filename):
    directory=os.path.join(app.root_path,'static/images')
    # filename='moon.jpg'
    return send_from_directory(directory=directory,filename=filename)

@app.route('/gallery')
@login_required
def gallery():
    directory = os.path.join(app.root_path,'static/images')
    images = os.listdir(directory)
    return render_template('gallery.html', images=images)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded, idot')
            return redirect(url_for('upload'))
        file = request.files['file']
        if file.filename == '':
            flash('No file uploaded, idiot')
            return redirect(url_for('upload'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            flash('{} saved in our gallery'.format(filename))
            return redirect(url_for('upload', filename=filename))
    return render_template('upload.html', title='Upload File')

# round entry form
@app.route('/enter_round', methods=['GET', 'POST'])
@login_required
def enter_round():
    player = ('Adam Simon')
    form = EnterRoundForm()
    if request.method == "POST":
        print(form.errors)
        round_obj = Round(playername = player,
                    courseid = 1,# need to check courses table for name
                    dateplayed = form.dateplayed.data,
                    slope = form.slope.data,
                    rating = form.rating.data,
                    strokes_front = form.strokes_front.data,
                    strokes_back = form.strokes_back.data,
                    strokes_total = int(form.strokes_front.data) + int(form.strokes_back.data),
                    putts_front = form.putts_front.data,
                    putts_back = form.putts_back.data,
                    putts_total = int(form.putts_front.data) + int(form.putts_back.data),
                    handicap = form.handicap.data,
                    quota = form.quota.data,
                    )
        db.session.add(round_obj)
        db.session.commit()
        flash("You're round at {} on {} has been submitted to the GateKeeper".format(form.coursename.data, form.dateplayed.data))
        return redirect(url_for('index'))
    return render_template('enter_round.html',
                            title='Enter Round',
                            player=player,
                            form=form)

@app.route('/alexa_flash')
@login_required
def alexa_flash():
    json_data = exportable_json
    return Response(response=json_data, mimetype='application/json')

@app.route('/downloads')
@login_required
def download_file():
    directory=os.path.join(app.root_path,'downloads')
    return send_from_directory(directory=directory,filename='dist.zip')

