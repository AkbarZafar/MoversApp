import os
import boto3

from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from validate_email import validate_email

app = Flask(__name__)

def getCipherSuite():
    key = (open('../supersecret.txt', 'r')).read()
    cipher_suite = Fernet(key)
    return cipher_suite

cipher_suite = getCipherSuite()


USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users")
def get_user():
    email = request.args.get('email')
    requestPassword = request.args.get('password')

    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'email': { 'S': email }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    email = item.get('email').get('S')
    password = cipher_suite.decrypt(item.get('password').get('B')).decode()
    
    if password != requestPassword:
        return jsonify({'error': 'Incorrect Password'}), 404

    return jsonify({
        'email': email,
        'password': password,
        'status' : 0
    })



@app.route("/users", methods=["POST"])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')

    if not password or not email:
        return jsonify({'error': 'Please provide email and password.'}), 400


    pass_encrypt = cipher_suite.encrypt(password.encode())
    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'email': {'S': email },
            'password': {'B': pass_encrypt },
        }
    )

    return jsonify({
        'email': email,
    })
