from flask_restful import Resource
from flask import request
from functools import wraps
import jwt
import os

SECRET_KEY = os.environ['API_SECRET']

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            raise RuntimeError('Token is missing')
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            raise RuntimeError('Token is invalid')

        
        clinic_id = request.args.get('clinic_id')
        if clinic_id and not (int(clinic_id) == int(data['clinic'])):
            raise RuntimeError('User does not have permissions to access clinic %s', clinic_id)
        
        return func(*args, **kwargs)
    return wrapper

class AuthResource(Resource):
    method_decorators = [authenticate]