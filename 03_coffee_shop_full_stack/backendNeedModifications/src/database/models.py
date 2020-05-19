import os
from flask import Flask
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

"""
def create_app():
is for the shell
https://python-decompiler.com/article/2013-10/when-scattering-
flask-models-runtimeerror-application-not-registered-on-db-w
"""

def create_app():
   #this func  is for the shell
    app = Flask(__name__)
    setup_db(app)
    db_drop_and_create_all()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:12@127.0.0.1:5432/coshop'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
'''drops the database tables and starts fresh
 can be used to initialize a clean database
 '''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()
'''this will initialize the database with some test drinks.

 called on every restart, after database has been reseted by db_drop_and_create_all()
 '''

def db_init_records():
    drink1 = (Drink(
                        id = 1,
                        title = 'milk shake',
                        recipe =
                                {
                                    "name" : "milk",
                                    "color": "grey",
                                    "parts": 1
                                }

                        ))

    drink2 = (Drink(
                        id = 2,
                        title = 'Purple Pain',
                        recipe =
                                {   
                                    "name" : "guave",
                                    "color": "purple",
                                    "parts": 3
                                }


                        ))

    new_drink3 = (Drink(
                    id = 3,
                    title = 'Rainbow Dash',
                    recipe = [
                            {
                                "name" : "cheery",
                                "color": "red",
                                "parts": 1
                            },
                            {
                                "name": "lemon",
                                "color": "yellow",
                                "parts": 1
                            },
                            {
                                "name": "apple",
                                "color": "green",
                                "parts": 1
                            },
                            {
                                "name": "blueberry",
                                "color": "blue",
                                "parts": 1
                            },
                            {
                                "name": "grape",
                                "color": "purple",
                                "parts": 1
                            }
                    ]
                    ))

    new_drink4 = (Drink(
                id = 4,
                title = 'Test',
                recipe = [
                        {
                            "name" : "cheery",
                            "color": "red",
                            "parts": 1
                        },
                        {
                            "name": "lemon",
                            "color": "yellow",
                            "parts": 1
                        },
                        {
                            "name": "",
                            "color": "white",
                            "parts": 1
                        }
                ]
                ))

    new_drink1.insert()
    #new_drink2.insert()
    #new_drink3.insert()
    #new_drink4.insert()

    print(new_drink1.short())
    print(new_drink1.long())





'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''

SIZE = 256
class TextPickleType(TypeDecorator):
    impl = sqlalchemy.String(SIZE)
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value


class Drink(db.Model):
    __tablename__ = 'drink'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)

    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe =Column(TextPickleType(), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''
    def short(self):
        """https://stackoverflow.com/questions/42354001/python-json-object-must-be-str-bytes-or-bytearray-not-dict/42354033
        json.loads take a string as input and returns a dictionary as output.
           json.dumps take a dictionary as input and returns a string as output."""
        #for test
        #print("##dumps##",json.dumps(self.recipe))
        #print("##loads##",json.loads(self.recipe))
        """[{"name": "cheery", "color": "red", "parts": 1},
         {"name": "lemon", "color": "yellow", "parts": 1},
         {"name": "", "color": "white", "parts": 1}]"""
        #d=json.dumps(self.recipe)
        #print("d is", d)
        #print("d type is", type(d)) #d is a string

        #print("hi its short")
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        try:
            return {
                'id': self.id,
                'title': self.title,
                'recipe': json.loads(self.recipe)
            }
        except:
            return {
                'id': self.id,
                'title': self.title,
                'recipe': self.recipe
            }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
