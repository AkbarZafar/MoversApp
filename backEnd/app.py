import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_current_user



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
  os.path.join(basedir, 'Movers.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)


@app.route('/')
def home():
  return jsonify(message='hello!')


@app.route('/box', methods=['GET'])
@jwt_required
def get_box_list():
  current_user = get_current_user()

  return jsonify(message=current_user)

  # if box:
  #   # get a single box
  #   return 1
  # else:
  #   return 2
  #   # get all the the boxes by that user.


# @app.route('/box', methods=['POST'])
# def 



@app.route('/users', methods=['POST'])
def create_user():
  email = request.json['email']

  test = User.query.filter_by(email=email).first()
  if(test):
    return jsonify(message='That email already exists')
  else:
    username = request.json['username']
    password = request.json['password']
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User created sucessfully")


@app.route('/login', methods=['GET'])
def login():
  email = request.json['email']
  password = request.json['password']

  test = User.query.filter_by(email=email, password=password).first()
  if test:
    access_token = create_access_token(identity=email)
    return jsonify(message= 'login suceeded', access_token=access_token)
  else:
    return jsonify(message='wrong credentials')




# database models
class User(db.Model):
  __tablename__ = 'Users'

  id = Column(Integer, primary_key=True)
  username = Column(String)
  email = Column(String, unique=True)
  password = Column(String)


class Boxes(db.Model):
  __tablename__ = 'Boxes'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  user = Column(ForeignKey('Users.id'))
  items = relationship('Items')


class Items(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String)
  box_id = Column(Integer, ForeignKey('Boxes.id'))

# database creation
@app.route('/db_create')
def create_db():
  db.create_all()
  return 'database created'

if __name__ == "__main__":
  app.run(debug=True)
