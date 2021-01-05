from flask_restful import Resource
from flask import request

class Foo(Resource):
    def get(self):
        bar = request.args.to_dict()
        print(bar)
        return bar