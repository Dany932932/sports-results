from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/sports_results.db'
db = SQLAlchemy(app)

class SportResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(50), nullable=False)
    team1 = db.Column(db.String(50), nullable=False)
    team2 = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

db.create_all()

@app.route('/')
def index():
    results = SportResult.query.all()
    return render_template('index.html', results=results)

@app.route('/add', methods=['GET', 'POST'])
def add_result():
    if request.method == 'POST':
        sport = request.form['sport']
        team1 = request.form['team1']
        team2 = request.form['team2']
        score = request.form['score']
        date = request.form['date']
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        new_result = SportResult(sport=sport, team1=team1, team2=team2, score=score, date=date)
        db.session.add(new_result)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_result.html')

@app.route('/count')
def count_results():
    count = SportResult.query.count()
    return f"Total number of results: {count}"

@app.route('/sport/<sport_name>')
def results_by_sport(sport_name):
    results = SportResult.query.filter_by(sport=sport_name).all()
    return render_template('results_by_sport.html', results=results, sport=sport_name)

if __name__ == '__main__':
    app.run(debug=True)
