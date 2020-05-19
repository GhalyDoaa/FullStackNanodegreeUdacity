import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
"""
https://2.python-requests.org/en/v1.0.4/user/quickstart/
"""


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    #paginate function
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    """ tested by :
    def test_error_405_get_all_categories(self):
    def test_error_405_get_all_categories(self):  
     """

    #to get all available categories
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # page = request.args.get('page', 1, type=int)
        # start = (page - 1) * 3
        # end = start + 3
        categories = Category.query.all()
        if not categories:
            abort(404)

        formated_categories = [categorie.format() for categorie in categories]
        categories_returned = []
        categories_returned.append([y["type"] for y in formated_categories])

        return jsonify({

            'success': True,
            'categories': categories_returned,
            'total_categories': len(formated_categories)

        })

    """ tested by :
    def test_get_all_questions_paginated
    def test_get_all_questions_paginated
    def test_error_404_get_all_questions_paginated(self):
    def test_error_405_get_all_questions_paginated(self):
     """

    # to get all available questions
    @app.route('/questions', methods=['GET'])
    def get_questions():

        questions = Question.query.all()
        formated_questions = [question.format() for question in questions]
        categories = Category.query.all()
        formated_categories = [categorie.format() for categorie in categories]
        # Initialize empty list to be filled & return only type column
        categories_returned = []
        categories_returned.append([y["type"] for y in formated_categories])
        return jsonify({

            'success': True,
            'questions': formated_questions,
            'total_questions': len(formated_questions),
            'categories': categories_returned,
            'current_category': categories_returned

        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    """
     tested by 
    def test_404_delete_question(self):
    def test_delete_question(self):

     
    """
    #to delete  a specified question using its id
    @app.route('/questions/<int:qid>', methods=['DELETE'])
    def delete_question(qid):

        try:
            question = Question.query.filter(Question.id == qid).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': qid,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''



    """
    tested by
    
    def test_create_question(self):

    """
    #to create new question
    @app.route('/newquestion', methods=['POST'])
    def create_question():
        body = request.get_json()
        if not body:
            abort(404)
        question = body.get('question')
        answer = body.get('answer')
        category_id = body.get('category_id')
        difficulty = body.get('difficulty')
        """
        curl -iX POST  http://127.0.0.1:5000/question  -H "Content-Type:application/json" -d '{"question":"Big and White Can walk Cant talk?", "answer":"the moon","category_id":"5","difficulty":"4"}'
        """
        if not question:
            abort(400)

        if not answer:
            abort(400, {'message': 'Answer can not be blank'})

        if not category_id:
            abort(400, {'message': 'Category can not be blank'})

        if not difficulty:
            abort(400, {'message': 'Difficulty can not be blank'})

        try:
            newQuestion = Question(question=question, answer=answer, category_id=category_id, difficulty=difficulty)
            newQuestion.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': newQuestion.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    """
    tested by 
    def test_search_question(self):
    def test_error_404_search_question(self):
    """
    #to search within all questions for a spaific word
    @app.route('/searchquestions', methods=['POST'])
    def search_questions():
        body = request.get_json()
        if not body:
            abort(404)
        search = body.get('search')
        selection = Question.query.filter(Question.question.contains(search)).all()
        current_questions = paginate_questions(request, selection)

        if not selection:
            return jsonify({

                'success': False,
                'questions': current_questions,
                'message': 'no matching found'

            })
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category':categories_all

        })

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    #to get all questions in a certain category
    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def get_questions_within_category(cat_id):

        category = Category.query.filter(Category.id == cat_id).one_or_none()
        selection = Question.query.filter(Question.category_id == cat_id).all()
        if not selection:
            abort(400)
        questions_paginated = paginate_questions(request, selection)
        cats = Category.query.all()
        formated_category = [cat.format() for cat in cats]

        if len(questions_paginated) == 0:
            abort(404)


        return jsonify({
            'success': True,
            'questions': questions_paginated,
            'total_questions': len(selection),
            'current_category': category.format(),
            'categories': formated_category

        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    """
    tested by:-
    def test_play_quiz_with_category(self):
    def test_play_quiz_without_category(self):
    def test_error_400_play_quiz(self):
    def test_error_405_play_quiz(self):

    """
    @app.route('/play', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        if not body:
            abort(400, {"message": "Please provide a JSON body with previous question Ids and optional category."})
        previous_questions = body.get('previous_questions', None)
        current_category = body.get('quiz_category', None)

        if not previous_questions:
            if current_category:
                selection = Question.query.filter(Question.category_id == current_category).all()
            else:

                selection = Question.query.all()
        else:
            if current_category:
                # testby
                # curl -iX POST  http://127.0.0.1:5000/play -H "Content-Type:application/json"  -d '{"previous_questions":["3","10"],"quiz_category":"2"}'

                selection = Question.query.filter(Question.category_id == current_category).filter(
                    Question.id.notin_(previous_questions[:])).all()
            else:

                selection = Question.query.filter(Question.id.notin_(previous_questions)).all()

        randGenerator = random.randint(0, len(selection) - 1)
        formated_questions = [q.format() for q in selection]
        Qobject = formated_questions[randGenerator]

        return jsonify({
            'previous_questions':previous_questions,
            'success': True,
            'question': Qobject
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"

        }), 400

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

