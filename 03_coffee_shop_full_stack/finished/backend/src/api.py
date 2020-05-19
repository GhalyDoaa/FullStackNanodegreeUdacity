'''https://www.reddit.com/r/flask/comments/4qdq7b/sqlalchemy_help_how_to_make_manytomany/'''
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()
''' custom error function'''
def get_error_message(error, default_text):
    try:
        # Return message contained in error, if possible
        return error['description']
    except TypeError:
        # otherwise, return given default text
        return default_text
'''GET /drinks public endpoint
        it should contain only the drink.short() data representation'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    # if there is drinks
    if drinks:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }), 200
    # if no drinks
    return jsonify({
        "success": False,
        "code": 404,
        "message": "no drinks found "
    }), 404
'''GET /drinks-detail 'get:drinks-detail' permission contain the drink.long() data representation
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(jwt):
    drink = Drink.query.all()
    drinks = [d.long() for d in drink]
    if drinks:
        return jsonify({
            "success": True,
            "code": 200,
            "drink": drinks
        }), 200

    return jsonify({
        "success": False,
        "code": 404,
        "message": "no drinks found "
    }), 404
'''POST /drinks create a new row in the drinks table
        it should require the 'post:drinks' permission'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    if not body:
        abort(404, {"message": "no body found"})
    try:
        req_recipe = body['recipe']
        if isinstance(req_recipe, dict):
            req_recipe = [req_recipe]
        drink = Drink()
        drink.title = body['title']
        drink.recipe = json.dumps(req_recipe)  # convert object to a string
        drink.insert()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })
'''
PATCH /drinks/<id> where <id> is the existing model id respond with a 404 error if <id> is not found
      ,update the corresponding row for <id>,require the 'patch:drinks' permission
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    body = request.get_json()
    print("your body is", body)
    if not body:
        abort(400, {'message': 'request does not contain a valid JSON body.'})

    updated_title = body.get('title', None)
    updated_recipe = body.get('recipe', None)
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink:
        abort(404)
    # Depending on which fields are available, make accorisbonding updates
    if updated_title:
        drink.title = body['title']
    if updated_recipe:
        drink.recipe = json.dumps(req['recipe'])

    drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })
''' 
DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found, delete the corresponding row for <id>,require the 'delete:drinks' permission
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    if not id:
        abort(404, {'message': 'Drink with id {} not found in database.'.format(id)})
    drinkis = Drink.query.filter(Drink.id == id).one_or_none()
    if not drinkis:
        abort(404)
    drinkis.delete()
    return jsonify({
        "success": True,
        "delete": id
    }), 200
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": get_error_message(error, "unprocessable")
    }), 422
'''
 error handler for 404
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": get_error_message(error, "resource not found")
    }), 404
@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": get_error_message(AuthError.error, "authentification fails")
    }), 401
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405