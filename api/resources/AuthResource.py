from flask_restful import Resource
from flask import request
from functools import wraps
import jwt
import os


SECRET_KEY = os.environ['API_SECRET']


class Unauthorized(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            raise Unauthorized("A valid authentication token is required for this route.")

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise Unauthorized("A valid authentication token is required for this route.")

        clinic_id = request.args.get('clinic_id')
        print(clinic_id == data['clinic'])
        if clinic_id and not (int(clinic_id) == int(data['clinic'])):
            raise Unauthorized('User does not have permissions to access clinic %s', clinic_id)

        return func(*args, **kwargs)
    return wrapper


class AuthResource(Resource):
    method_decorators = [authenticate]