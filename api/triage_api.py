""" The Triage API to serve to the front end """

''' Read the documentation from Flask: https://flask-restful.readthedocs.io/en/latest/'''
from flask import Flask
from flask_restful import Api
from resources.predict import Predict

app = Flask(__name__)
api = Api(app)

api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)