import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random
from flask_paginate import Pagination, get_page_parameter

from model import setup_db, Book

bookPerPag = 3
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_books(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * bookPerPag
        end = start + bookPerPag

        books = [book.format() for book in selection]
        current_books = books[start:end]

        return current_books

    #@app.route('/books/s/<book_title>',methods=['GET'])
    # def search_book(book_title):
    #     try:
    #         book = Book.query.filter(Book.title == book_title).all()
    #         if book is None:
    #             abort(404)
    #         return jsonify({
    #             'success': True,
    #             'book': book.format(),
    #             'total_books':len(book)
    #         })
    #     except:
    #         abort(400)



    @app.route('/books', methods=['GET'])
    def get_books():
        # page = request.args.get('page', 1, type=int)
        # page = request.args.get(get_page_parameter(), type=int, default=1)

        # start = (page - 1) * bookPerPag
        # end = start + bookPerPag

        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)
        if len(current_books) == 0:
            abort(404)
        # lth=Book.query.count()
        # formated = [book.format() for book in books]
        # will be ok with frontend
        # https://pythonhosted.org/Flask-paginate/
        # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
        # https://riptutorial.com/flask/example/22201/pagination-route-example-with-flask-sqlalchemy-paginate
        # pagination=Pagination (page=page, total=lth,per_page=2)

        return jsonify({
            'success': True,
            'Books': current_books,
            'total_books': len(selection)

        })

    # https://www.codepedia.org/ama/how-to-test-a-rest-api-from-command-line-with-curl/
    # curl  http://0.0.0.0:5000/books?page=4
    # curl -H "Accept:application/xml"  http://0.0.0.0:5000/books

    # curl  http://0.0.0.0:5000/books/2 -X PATCH -H "Content-Type:application/json" -d '{"rating":"5"}'

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def updatebook(book_id):
        body = request.get_json()
        try:
            bookis = Book.query.filter(Book.id == book_id).one_or_none()
            if bookis is None:
                abort(404)

            if 'rating' in body:
                bookis.rating = int(body.get('rating'))
                bookis.update()

            return jsonify({
                'success': True,
                'book': bookis.id
            })
        except:
            abort(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            book.delete()
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'total_books': len(Book.query.all())
            })

        except:
            abort(422)
#curl -X GET http://127.0.0.1:5000/books/s/apple
#curl -X GET -d '{search:"apple"}'  http://127.0.0.1:5000/books/s/apple


    @app.route('/books/s/<search>', methods=['POST', 'GET'])
    def search_book(search):
            #body = request.get_json()
        print("hello from search route")
        search_title= search
        selection = Book.query.filter(Book.title.ilike('%{}%'.format(search_title)))
        current_books = paginate_books(request, selection)

        return jsonify({
                'success': True,
                'books': current_books,
                'total_books': len(selection.all())

            })


    @app.route('/books', methods=['POST'])
    def create_book():

            body = request.get_json()
            new_title = body.get('title',None)
            new_author = body.get('author',None)
            new_rating = body.get('rating',None)
            #search=body.get('search', None)
            try:
                # if search:
                #    ## search_book()##
                #     # selection=Book.query.filter(Book.title.ilike('%{}%'.format(search)))
                #     # current_books=paginate_books(request,selection)
                #     #
                #     # return jsonify({
                #     #     'success':True,
                #     #     'books': current_books,
                #     #     'total_books':len(selection.all())
                #     #
                #     # })
                # else:
                    book = Book(title=new_title, author=new_author, rating=new_rating)
                    book.insert()

                    selection = Book.query.order_by(Book.id).all()
                    current_books = paginate_books(request, selection)

                    return jsonify({
                     'success': True,
                        'created': book.id,
                           'books': current_books,
                         'total_books': len(Book.query.all())
                 })

            except:
                abort(422)



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
            "message": "method not found"
        }), 405





    return app



"""
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
"""