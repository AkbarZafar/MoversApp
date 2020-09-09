import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_marshmallow import Marshmallow


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'Movers.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)


@app.route('/')
def home():
    return jsonify(message='hello!')


# Routes for boxes
@app.route('/box', methods=['POST'])
@jwt_required
def create_box():
    # checks if a box under qr code exists,
    # if it exists, retrieve, if not create a box.

    # user_email = get_jwt_identity()
    # user_id = User.query.filter_by(email=user_email).first().id

    # qr_code = request.json['qr_code']
    # box_id = request.json['box_id']

    # box = Boxes(room_name=room_name, user_id=user_id)
    # db.session.add(box)
    # db.session.commit()

    return jsonify(message="Box created sucessfully")


@app.route('/box', methods=['GET'])
@jwt_required
def get_box_items():
    user_email = get_jwt_identity()
    user_id = User.query.filter_by(email=user_email).first().id

    qr_code = request.json['qr_code']
    box_id = request.json['box_id']
    if qr_code:
        box_id = Boxes.query.filter_by(
            user_id=user_id, qr_code=qr_code).first().id

    items = Items.query.filter_by(box_id=box_id)
    if items:
        result = items_schema.dump(items)
        return jsonify(result)
    else:
        return  jsonify('create new box')


@app.route('/all_boxes', methods=['GET'])
@jwt_required
def get_box_list():
    user_email = get_jwt_identity()
    user_id = User.query.filter_by(email=user_email).first().id
    # returns all boxes for current user.
    boxes = Boxes.query.filter_by(user_id=user_id)

    result = boxes_schema.dump(boxes)
    return jsonify(result.data)


# routes for users
@app.route('/register', methods=['POST'])
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


@ app.route('/login', methods=['GET'])
def login():
    email = request.json['email']
    password = request.json['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='login suceeded', access_token=access_token)
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
    qr_code = Column(String(6))
    room_name = Column(String)
    box_name = Column(String)
    user_id = Column(ForeignKey('Users.id'))


class Items(db.Model):
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    box_id = Column(Integer, ForeignKey('Boxes.id'))


# Schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class BoxesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'room_name', 'box_name', 'user_id')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item_name', 'box_id')


user_schema = UserSchema()

boxes_schema = BoxesSchema(many=True)

items_schema = ItemSchema(many=True)

# database creation


@app.route('/db_create')
def create_db():
    db.create_all()
    return jsonify(message='database created')


@app.route('/db_seed')
def seed_db():
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
        room_name='living_room',
        box_name='tv stuff',
        qr_code='000001',
        user_id=1,
    )

    dining_room = Boxes(
        room_name='dining_room',
        box_name='decor items',
        qr_code='000000',
        user_id=1
    )

    pillow = Items(
        item_name='pillow',
        box_id=1
    )

    bedsheets = Items(
        item_name='bedsheets',
        box_id=1
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(living_room)
    db.session.add(dining_room)
    db.session.add(pillow)
    db.session.add(bedsheets)

    db.session.commit()
    return jsonify(message='database seeded')


@app.route('/db_drop')
def drop_db():
    db.drop_all()
    return jsonify(message='database dropped')


if __name__ == "__main__":
    app.run(debug=True)
