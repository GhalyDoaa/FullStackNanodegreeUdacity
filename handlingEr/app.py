from flask import Flask, request, abort, jsonify
import os
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12@127.0.0.1:5432/plantapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
migrate = Migrate(app, db)

CORS(app)

db.app = app
db.init_app(app)
db.create_all()


class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientific_name = db.Column(db.String)
    is_poisonous = db.Column(db.Boolean, default=False)
    primary_color = db.Column(db.String)

    def __init__(self, name, scientific_name, is_poisonous, primary_color):
        self.name = name
        self.scientific_name = scientific_name
        self.is_poisonous = is_poisonous
        self.primary_color = primary_color

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'is_poisonous': self.is_poisonous,
            'primary_color': self.is_poisonous
        }


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response


@app.route('/plants', methods=['GET', 'POST'])
def get_plants():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 3
    end = start + 3
    plants = Plant.query.all()
    formated_plants = [plant.format() for plant in plants]
    return jsonify({
        'success': True,
        'plants': formated_plants[start:end],
        'total plants': len(formated_plants)

    })


@app.route('/plants/<int:plant_id>', methods=['GET'])
def getplant(plant_id):
    plant = Plant.query.get(plant_id)
    if plant is None:
        abort(404)
    else:

        formated_plant = plant.format()

        return jsonify({
        'success': True,
        'plant': formated_plant

    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
