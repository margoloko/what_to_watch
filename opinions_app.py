from datetime import datetime
from random import randrange
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return 'none opinion'
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)

@app.route('/add')
def add_opinion_view():
    return render_template('add_opinion.html')

@app.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get(id)
    return render_template('opinion.html', opinion=opinion)

if __name__ == '__main__':
    app.run()
