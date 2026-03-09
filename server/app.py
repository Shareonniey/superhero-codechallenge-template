#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{
       "id": hero.id,
       "name": hero.name,
       "super_name": hero.super_name
    }
    for hero in heroes
    ]
    return jsonify(hero_list), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
     return jsonify(hero.to_dict()), 200
    return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [
       {
          "id": power.id,
          "name": power.name,
          "description": power.description
       }
       for power in powers
    ]
    return jsonify(power_list), 200

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify({
       "id": power.id,
       "name": power.name,
       "description": power.description
    }), 200

    return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
     return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    
    try:
       power.description = data.get('description')
       db.session.commit()
       
       return jsonify({
          "id": power.id,
          "name": power.name,
          "description": power.description
       }), 200
    except Exception:
        return jsonify({'errors': ['validation errors']}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')
    
    if not all([hero_id, power_id, strength]):
       return jsonify({'errors': ['All fields are required']}), 400
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
       return jsonify({'errors': ['Invalid hero_id or power_id']}), 400
    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify({
       "id": hero_power.id,
       "strength": hero_power.strength,
       "hero_id": hero_power. hero_id,
       "power_id": hero_power.power_id,
       "hero": hero_power.hero.to_dict(),
       "power": hero_power.power.to_dict()
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
