from flask_restful import Resource
from flask import request
import psycopg2

class Models(Resource):
    def get(self):
        args = request.args.to_dict()
        try:
            clinic_id = int(args['clinic-id'])
        except:
            return {'status': 400}
        db = psycopg2.connect(
                database="triage", 
                user="admin", 
                password="docker", 
                host="localhost", 
                port="5432"
            )
        cur = db.cursor()
        cur.execute(f"SELECT id, accuracy, to_char(created,'DD-MM-YYYY'), in_use \
                      FROM triagedata.models \
                      WHERE clinic_id={clinic_id}")
        rows = cur.fetchall()
        db.close()
        return {'status': 200, 'models': [('id', 'accuracy', 'created', 'in_use')] + rows}

class Use(Resource):
    def patch(self):
        args = request.args.to_dict()
        try:
            clinic_id = int(args['clinic-id'])
            model_id = int(args['model-id'])
        except:
            return {'status': 400}
        db = psycopg2.connect(
                database="triage", 
                user="admin", 
                password="docker", 
                host="localhost", 
                port="5432"
            )        
        cur = db.cursor()
        cur.execute(f"UPDATE triagedata.models \
                      SET in_use = (CASE WHEN id={model_id} THEN true \
                                         ELSE false \
                                    END) \
                      WHERE clinic_id={clinic_id}")
        db.commit()
        db.close()
        return {'status': 200}
