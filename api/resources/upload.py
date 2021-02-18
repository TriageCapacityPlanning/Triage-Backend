from flask_restful import Resource
from flask import request


class Waitlist(Resource):
    def put(self):
        raise NotImplementedError()


class PastAppointments(Resource):
    def put(self):
        raise NotImplementedError()
