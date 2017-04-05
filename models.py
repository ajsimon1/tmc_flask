from __init__ import db

class Player(db.Model):
    playerid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    nickname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cellphone = db.Column(db.Integer, nullable=True)
    handicap = db.Column(db.Integer, nullable=True)
    quota = db.Column(db.Integer, nullable=True)
    avg_strokes = db.Column(db.Integer, nullable=True)
    avg_putts = db.Column(db.Integer, nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.playerid)

    def __repr__(self):
        return '<{firstname} {lastname}, {handicap}>'.format(
                                                        self.firstname,
                                                        self.lastname,
                                                        self.handicap)
class Course(db.Model):
    courseid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coursename = db.Column(db.String(255), nullable=False)
    coursecity = db.Column(db.String(25), nullable=False)
    coursestate = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<{coursename}({courseid}) in {coursecity}, {coursestate}>'.format(
                                                        self.coursename,
                                                        self.courseid,
                                                        self.coursecity,
                                                        self.coursestate)

class Teebox(db.Model):
    teeboxeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseid = db.Column(db.Integer, db.ForeignKey('course.courseid'), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    slope = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<{color} teebox for course ID {courseid}>'.format(
                                                        self.color,
                                                        self.courseid)

class Round(db.Model):
    roundid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerid = db.Column(db.Integer, db.ForeignKey('player.playerid'), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey('course.courseid'), nullable=False)
    dateplayed = db.Column(db.Date, nullable=False)
    slope = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    strokes_front = db.Column(db.Integer, nullable=False)
    strokes_back = db.Column(db.Integer, nullable=False)
    strokes_total = db.Column(db.Integer, nullable=False)
    putts_front = db.Column(db.Integer, nullable=False)
    putts_back = db.Column(db.Integer, nullable=False)
    putts_total = db.Column(db.Integer, nullable=False)
    quota = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<round {roundid} played on {dateplayed} at {courseid}. Shot {strokes_total} with {quota} quota>'.format(
                                                                self.roundid,
                                                                self.dateplayed,
                                                                self.courseid,
                                                                self.strokes_total,
                                                                self.quota)
