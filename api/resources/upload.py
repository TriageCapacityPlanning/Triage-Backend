from flask_restful import Resource
from flask import request


class Waitlist(Resource):
    def put(self):
        args = request.args.to_dict()
        print(request.files)
        return args


class PastAppointments(Resource):
    def put(self):
        args = request.args.to_dict()
