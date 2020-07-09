from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidates.sqlite3'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)


class Candidates(db.Model):
    __tablename__ = 'gen_entitylistings2020'
    __table_args__ = {'extend_existing': True}
    NAME = db.Column(db.Text, primary_key=True)


@app.route('/')
def index():
    candidate_count = Candidates.query.count()
    loc_candidacy = Candidates.query.all()
    return render_template('index.html', count=candidate_count, loc_candidacy=loc_candidacy, location="New Jersey")


@app.route('/candidates/<slug>')
def detail(slug):
    loc_candidacy = Candidates.query.filter_by(SLUG=slug).first()
    return render_template('detail.html', loc_candidacy=loc_candidacy)

@app.route('/location/<locationname>')
def location(locationname):
    locationname = locationname.replace('-', ' ')
    locations = Candidates.query.filter_by(LOCATION=locationname.upper()).all()
    return render_template('index.html', locations=locations, count=len(locations), location=locationname, loc_candidacy=locations)


@app.route('/location')
def location_list():
    locations = Candidates.query.with_entities(Candidates.LOCATION).distinct().all()
    locations = [LOCATION[0] for LOCATION in locations]
    return render_template("locations.html", locations=locations)


# if __name__ == '__main__':
#   app.run(debug=False)

def getApp():
    return app
