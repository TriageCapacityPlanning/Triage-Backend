from flask_restful import Resource
from flask import request
from triage_models.load_and_predict import load_and_predict_patient_total
import json
import math

class Predict(Resource):
    def get(self):
        args = request.args.to_dict()
        return self.buildPrediction(args)

    def buildPrediction(self, args):
        totalPatients = load_and_predict_patient_total(int(args['predictionLengthDays']))
        totalSlots = int(args['dailySlotsAvailable']) * int(args['predictionLengthDays'])
        expectedPatientsPerTriageClass = self.calculateTriageDistribution(totalPatients)
        slotsPerTriageClass = self.calculateSlotsDistribution(totalSlots, expectedPatientsPerTriageClass, float(args['percentageOfUrgentPatients'])/100)
        patientsSeenPercentage = self.calculatePatientsSeenPercentage(expectedPatientsPerTriageClass, slotsPerTriageClass)

        return {
            'totalPatients': totalPatients,
            'totalSlots': totalSlots,
            'expectedPatientsPerTriageClass': expectedPatientsPerTriageClass,
            'slotsPerTriageClass': slotsPerTriageClass,
            'patientsSeenPercentage': patientsSeenPercentage
        }

    def calculateSlots(self, predictionLengthDays):
        return 2 * predictionLengthDays
    
    def calculateTriageDistribution(self, totalPatients):
        patientDistribution = {
            'urgent': 0.2,
            'semi-urgent': 0.3,
            'standard': 0.5
        }

        return {
            'urgent': int(totalPatients * patientDistribution['urgent']),
            'semi-urgent': int(totalPatients * patientDistribution['semi-urgent']),
            'standard': int(totalPatients * patientDistribution['standard'])
        }
    
    def calculateSlotsDistribution(self, totalSlots, expectedPatientsPerTriageClass, percentageOfUrgentPatients):
        minUrgentSlots = min(totalSlots, math.ceil(expectedPatientsPerTriageClass['urgent'] * percentageOfUrgentPatients))
        semiUrgentSlots = min(int((totalSlots - minUrgentSlots) / 2), expectedPatientsPerTriageClass['semi-urgent'])
        standardSlots = min(totalSlots - minUrgentSlots - semiUrgentSlots, expectedPatientsPerTriageClass['standard'])
        urgentSlots = min(max(totalSlots - semiUrgentSlots - standardSlots, minUrgentSlots), expectedPatientsPerTriageClass['urgent'])

        return {
            'urgent': urgentSlots,
            'semi-urgent': semiUrgentSlots,
            'standard': standardSlots
        }
    
    def calculatePatientsSeenPercentage(self, expectedPatientsPerTriageClass, slotsPerTriageClass):
        return {
            'urgent': slotsPerTriageClass['urgent'] / expectedPatientsPerTriageClass['urgent'],
            'semi-urgent': slotsPerTriageClass['semi-urgent'] / expectedPatientsPerTriageClass['semi-urgent'],
            'standard': slotsPerTriageClass['standard'] / expectedPatientsPerTriageClass['standard'],
        }
