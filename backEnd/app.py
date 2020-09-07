from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
  os.path.join(basedir, 'Movers.db')

db = SQLAlchemy(app)


def db_create():
  db.create_all()
  print('DB CREATED')


# @app.cli_command('db_drop')
# def db_drop():
#   db.drop_all
#   print('DB DROPPED')


def db_seed():
  user1 = User(
    username='User1',
    email='email@email.com',
    password='p@ss'
  )
  user2 = User(
    username='User2',
    email='email2@email2.com',
    password='p@ssw0rd'
  )

  living_room = Boxes(
    name='living_room',
    user=user1,
  )

  dining_room = Boxes(
    name='dining_room',
    user=user1
  )

  pillow = Items(
    name='pillow',
    box_id=1
  )

  bedsheets = Items(
    name='bedsheets',
    box_id=1
  )

  db.session.add(user1)
  db.session.add(user2)
  db.session.add(living_room)
  db.session.add(dining_room)
  db.session.add(pillow)
  db.session.add(bedsheets)

  db.session.commit()
  print('DB SEEDED')

@app.route('/')
def home():
  return jsonify(message='hello!')


@app.route('/box')
def get_box_list():
  userID = int(request.args.get('userID'))
  box = request.args.get('box')

  if box:
    # get a single box
    return 1
  else:
    return 2
    # get all the the boxes by that user.


# database models
class User(db.Model):
  __tablename__ = 'Users'

  id = Column(Integer, primary_key=True)
  username = Column(String)
  email = Column(String, unique=True)
  password = Column(String)


class Boxes(db.Model):
  __tablename__ = 'Boxes'

  id = Column(Integer, primart_key=True)
  name = Column(String)
  user = Column(ForeignKey('Users.id'))
  items = relationship('Items')


class Items(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String)
  box_id = Column(Integer, ForeignKey('Boxes.id'))


if __name__ == "__main__":
  app.run(debug=True)
