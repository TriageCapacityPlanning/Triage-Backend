from api.common.exceptions import Unauthorized
from flask_restful import Resource
from flask import request
from functools import wraps
import jwt
import os


SECRET_KEY = os.environ['API_SECRET']


def authenticate(func):
    """
    A function decorator for protecting functions that require authentication to access.
    """
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
        if clinic_id and not (int(clinic_id) == int(data['clinic'])):
            raise Unauthorized('User does not have permissions to access clinic %s', clinic_id)

        return func(*args, **kwargs)
    return wrapper


class AuthResource(Resource):
    """
    An inheritance class for auth protected endpoints
    """
    method_decorators = [authenticate]
