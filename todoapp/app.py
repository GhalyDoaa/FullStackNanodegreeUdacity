'''
Created on Jan 26, 2020

@author: hardy
'''
from flask import Flask, abort, render_template, jsonify, flash, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12@127.0.0.1:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True , cascade="save-update, merge, delete , all , delete-orphan")


order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}, list {self.list_id}>'

# db.create_all()

@app.route('/todolists/<listtodoId>', methods=['POST'])
def checked_list(listtodoId):
    try:
        chk = request.get_json()['completed']
        #print("this is completed", 'completed', chk)
        # thats is True
        print("thats is" , chk)
        listtodo = TodoList.query.get(listtodoId)
        print(listtodo)
        #user1 = sess1.query(User).filter_by(id=1).first()
        chec=Todo.query.filter(Todo.list_id==listtodoId)
        for c in chec:
            c.completed=chk
            print(c)


        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def checked(todo_id):
    try:
        chk = request.get_json()['completed']
        print("this is completed", 'completed', chk)
        # thats is False
        # print("thats is" , chk)
        todo = Todo.query.get(todo_id)
        todo.completed = chk
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todolist/<listid>/delete', methods=['POST'] )
def delete_todolist(listid):
    try:
        Todo.query.filter(Todo.list_id == listid).delete()


        TodoList.query.filter(TodoList.id==listid).delete()
        db.session.commit()
    except:
        db.session.rollback()

    finally:
        db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/<itemid>', methods=['DELETE'])
def delete_todo(itemid):
    try:
        Todo.query.filter_by(id=itemid).delete()
        db.session.commit()
    except:
        db.session.rollback()

    finally:
        db.session.close()

    return redirect(url_for('index'))

@app.route('/todolists/create', methods=['POST'])
def create_list_todo():
    error = False
    body = {}
    try:
        # 'green' is the key of the json body from our ajax request
        # ajax req. sent as a dictionary
        new = request.get_json()['name']
        todolst = TodoList(name=new)
        db.session.add(todolst)
        db.session.commit()
        body['id'] = todolst.id
        body['name'] = todolst.name
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        print(jsonify(body))
        return jsonify(body)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # 'green' is the key of the json body from our ajax request
        # ajax req. sent as a dictionary
        description = request.get_json()['description']
       # tolist=TodoList.query.filter_by(name=cLst).first()

        todo = Todo(description=description, completed=False,list_id=1)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description


    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        print(jsonify(body))
        return jsonify(body)

@app.route('/lists/<list_id>')
#route to  a certain id number of the mail lists
# (the controler)route handler
def get_list_todos(list_id):
    return render_template('index.html',
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())




#old version
@app.route('/')
# (the controler)route handler
def index():
    #the main page shows the list1
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
    app.debug = 'True'
    app.run()
