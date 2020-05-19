import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_path = 'postgresql://postgres:12@127.0.0.1:5432/trivia'
        setup_db(self.app, database_path)
        self.new_Q = {
            'question': 'are you crazy?',
            'answer': 'of courseyou are :p',
            'category_id': 5,
            'difficulty': 2

        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    def test_create_question(self):
        """Test POST a new question """

        # Used as header to POST /question
        json_create_question = {
            'question': 'Is this a test question?',
            'answer': 'Yes it is!',
            'category_id': '1',
            'difficulty': 1
        }
        res = self.client().post('/newquestion', json=json_create_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'] > 0)


    def test_endpoint_not_available(self):
        """Test getting an endpoint which does not exist """
        res = self.client().get('/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test failed operation for /newquestion endpoint
    def test_error_create_question(self):
        json_create_question_error = {
            'question' : 'Is this a test question?',
            'answer' : 'Yes it is!',
            'difficulty' : 1
        }

        res = self.client().post('/newquestion', json = json_create_question_error)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    # test succsessful operation for /searchquestions endpoint
    def test_search_question(self):
        json_search_question = {
            'search' : 'gypt',
        }

        res = self.client().post('/searchquestions', json = json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    # test failed operation for /searchquestions endpoint

    def test_error_404_search_question(self):
        json_search_question = {
            'search': 'tzzzzinit'
        }

        res = self.client().post('/searchquestions', json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"no matching found")


    # test failed operation for /categories endpoint

    def test_error_405_get_all_categories(self):
        res = self.client().patch('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)


    # test successful operation for paginate the /questions endpoint

    def test_get_all_questions_paginated(self):
        res = self.client().get('/questions?page=1', json={'category:': 'science'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'] > 0)



    def test_error_405_get_all_questions_paginated(self):
        """Test wrong method to get all questions from all categories """
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)

    def test_error_404_get_all_questions_paginated(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        """Test DELETE /question """
        #1 create a new question so it can later be deleted

        # Used as header to POST /question
        json_create_question = {
            'question': 'are you hungry?',
            'answer': 'No!',
            'category_id': '1',
            'difficulty': 1
        }

        res = self.client().post('/newquestion', json=json_create_question)
        data = json.loads(res.data)
        question_id = data['created']

        #2  make a DELETE request with newly created question
        res = self.client().delete('/questions',json={'id': question_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)



    def test_404_delete_question(self):
        """Test failed DELETE /question """


        res = self.client().delete('/questions/8765456')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_play_quiz_with_category(self):
        """Test /play succesfully with given category """
        json_play_quizz = {
            'previous_questions': [3, 10],
            'quiz_category': 2
        }
        res = self.client().post('/play', json=json_play_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        # check if returned question is NOT in previous question list
        self.assertTrue(data['question']['id'] not in json_play_quizz['previous_questions'])

    def test_play_quiz_without_category(self):
        """Test /play succesfully without category"""
        json_play_quizz = {
            'previous_questions': [3,10]
        }
        res = self.client().post('/play', json=json_play_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['question'])
        #check if returned question is NOT in previous question
        self.assertTrue(data['question']['id'] not in json_play_quizz['previous_questions'])

    def test_error_400_play_quiz(self):
        """Test /play error without any JSON Body"""
        res = self.client().post('/play')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"bad request")

    def test_error_405_play_quiz(self):
        """Test /play error with wrong method"""
        res = self.client().get('/play')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
