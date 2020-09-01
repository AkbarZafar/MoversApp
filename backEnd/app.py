# app.py
from models import Schema
from Service import BoxesService
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
  return "Hello World!"


@app.route("/<name>")
def helloName(name):
  return "hello " + name

@app.route("/boxes", methods=['POST'])
def create_box():
  return BoxesService().create(request.get_json())

if __name__ == "__main__":
  Schema()
  app.run(debug=True)
