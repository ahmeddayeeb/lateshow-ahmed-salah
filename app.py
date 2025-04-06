from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    number = db.Column(db.Integer)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')

    def to_dict(self, include=None, exclude=None):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' and (include is None or k in include) and (exclude is None or k not in exclude)}

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    occupation = db.Column(db.String(50))
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')

    def to_dict(self, include=None, exclude=None):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' and (include is None or k in include) and (exclude is None or k not in exclude)}

class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))

    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return rating

    def to_dict(self, include=None, exclude=None):
        data = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' and (include is None or k in include) and (exclude is None or k not in exclude)}
        if 'episode' in include or include is None:
            data['episode'] = self.episode.to_dict(include=['id', 'date', 'number'])
        if 'guest' in include or include is None:
            data['guest'] = self.guest.to_dict(include=['id', 'name', 'occupation'])
        return data

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict(include=['id', 'date', 'number']) for episode in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode is None:
        return jsonify({'error': 'Episode not found'}), 404
    return jsonify(episode.to_dict(include=['id', 'date', 'number', 'appearances'], exclude=['_sa_instance_state'] ))

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict(include=['id', 'name', 'occupation']) for guest in guests])

from flask import request

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        episode_id = data['episode_id']
        guest_id = data['guest_id']
        rating = data['rating']

        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode:
            return jsonify({'errors': [f'Episode with id {episode_id} not found']}), 400
        if not guest:
            return jsonify({'errors': [f'Guest with id {guest_id} not found']}), 400

        appearance = Appearance(rating=rating, guest_id=guest_id, episode_id=episode_id)
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict(include=['id', 'rating', 'guest_id', 'episode_id', 'episode', 'guest'])), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    except KeyError as e:
        db.session.rollback()
        return jsonify({'errors': [f'Missing key: {str(e)}']}), 400
    except Exception as e:
        db.session.rollback()
        errors = [str(e)]
        if isinstance(e, ValueError) and "Rating must be between 1 and 5" in str(e):
            errors = ["Rating must be between 1 and 5"]
        return jsonify({'errors': errors}), 400

@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
