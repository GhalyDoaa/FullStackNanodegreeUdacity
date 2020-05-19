from app import create_app
from model import setup_db, Book
import unittest
import json

"""
1-review curl
2-pagination


"""



class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        # self.database_name="bookapp"
        self.client = self.app.test_client
        # use formate is much better
        database_path = 'postgresql://postgres:12@127.0.0.1:5432/bookapp'
        setup_db(self.app, database_path)
        self.new_book = {
            'title': 'alaan afham',
            'author': 'ahmed khaled',
            'rating': 7

        }

    def tearDown(self):
        # executed after each test
        pass

    def test_get_paginated_books(self):
        # to get the end point
        res = self.client().get('/books')
        # load the data using json.load from response
        data = json.loads(res.data)
        # check some respose body variables
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        # check there is a books in the list = ckeck the list has a length
        self.assertTrue(len(data['Books']))

    def test_404_sent_requesting_beyond_valid_page(self):
        #get tothis endpoint included a json body
        res = self.client().get('/books?page=1000', json={'rating': 1})
        data = json.loads(res.data)
        # check some of the response body vars
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_update_book_rating(self):

        res=self.client().patch('/books/2',json={'rating':1})
        data=json.loads(res.data)
        #make sure to select one or none
        book=Book.query.filter(Book.id==2).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        #check the value from the database=> if it really changed
        self.assertEqual(book.format()['rating'],1)


    def test_400_for_failed_update(self):
        res=self.client().patch('/books/100',json={'rating':2})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_book(self):
        res=self.client().delete('/books/1')
        data=json.loads(res.data)
        books = Book.query.all()
        print(" db val ", books)
        book=Book.query.filter(Book.id==1).one_or_none()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        books = Book.query.all()
        print(" db val ", books)
        self.assertEqual(book,None)

    def test_404_if_book_doesnot_found(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_book_search_with_results(self):
        res = self.client().post('/books',json={'title':'apple'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']),3)

    def test_get_book_search_without_results(self):
        res = self.client().post('/books',json={'title':'apple'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success' ,True])
        self.assertEqual(data['total_books'],0)
        self.assertEqual(len(data['books']),0)
    def test_create_new_book(self):
        res = self.client().post('/books',json=self.new_book)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['books'])

        #something wrong with this line
        #self.assertTrue(len(data['total_books']))

    def test_404_if_book_creation_not_allowed(self):
        res = self.client().post('/books/45',json=self.new_book)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'] ,'method not allowed')




























    if __name__ == "__main__":
        unittest.main()



"""The 405 Method Not Allowed error occurs when the web server is configured in a way that does not allow you to perform a specific action for a particular URL. It's an HTTP response status code that indicates that the request method is known by the server but is not supported by the target resource."""