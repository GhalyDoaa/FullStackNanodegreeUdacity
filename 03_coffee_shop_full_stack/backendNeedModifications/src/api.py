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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()
''' custom error function'''

def get_error_message(error, default_text):

    try:
        # Return message contained in error, if possible
        return error['description']
    except TypeError:
        # otherwise, return given default text
        return default_text


def get_all_drinks(recipe_format):

    # Get all drinks in database
    all_drinks = Drink.query.order_by(Drink.id).all()
    # Format with different recipe detail level
    if recipe_format.lower() == 'short':
        all_drinks_formatted = [drink.short() for drink in all_drinks]
    elif recipe_format.lower() == 'long':
        all_drinks_formatted = [drink.long() for drink in all_drinks]
    else:
        return abort(500, {'message': 'bad formatted function call. recipe_format needs to be "short" or "long".'})

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'no drinks found in database.'})
    
    # Return formatted list of drinks
    return all_drinks_formatted


## ROUTES
'''
#DONE#
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():

    if get_all_drinks('short') :
        return jsonify({
            "success": True,
            "code": 200,
            "drinks":  get_all_drinks('short')
        }), 200
    return jsonify({
        "success": False,
        "code": 404,
        "message": "no drinks found "
    }), 404



'''
#DONE#
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks
     or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(jwt):

    drink = Drink.query.all()
    drinks=[d.long() for d in drink]

    if drinks :
        return jsonify({
            "success": True,
            "code": 200,
            "drink":  get_all_drinks('long')
        }), 200

    return jsonify({
        "success": False,
        "code": 404,
        "message": "no drinks found "
    }), 404

'''
#DONE#
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()

    if not body:
        abort(404, {"message": "no body found"})
        #{}
    new_drink = Drink(title = body['title'], recipe = """""".format(body['recipe']))
    new_drink.insert()
    new_drink.recipe = body['recipe']


    return jsonify({
            'success': True,
            'Drinks':  Drink.long(new_drink)
        })



'''
#DONE#
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt,id):
    body = request.get_json()
    print("your body is", body)
    if not body:
        abort(400, {'message': 'request does not contain a valid JSON body.'})
    updated_title = body.get('title', None)
    updated_recipe = body.get('recipe', None)
    drink_to_update = Drink.query.filter(Drink.id == id).one_or_none()
    # Depending on which fields are available, make apropiate updates
    if updated_title:
        drink_to_update.title = body['title']

    if updated_recipe:
    #{}
        drink_to_update.recipe = """{}""".format(body['recipe'])

    drink_to_update.update()

    return jsonify({
    'success': True,
    'drinks': [Drink.long(drink_to_update)]
        })




'''
#DONE#
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt,id):
    if not id:
        abort(404, {'message': 'Drink with id {} not found in database.'.format(id)})

    drinkis = Drink.query.filter(Drink.id == id).one_or_none()

    if drinkis is None:
        abort(404)

    drinkis.delete()
    return jsonify({
               "success": True,
               "delete": id
            })







## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": get_error_message(error,"unprocessable")
                    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": get_error_message(error, "resource not found")
                    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": get_error_message(error, "resource not found")
                    }), 404
'''
#DONE#
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentification_failed(AuthError): 
    return jsonify({
                    "success": False, 
                    "error": AuthError.status_code,
                    "message": get_error_message(AuthError.error, "authentification fails")
                    }), 401

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
