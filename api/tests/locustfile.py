from locust import HttpUser, between, task
import random


class User(HttpUser):
    wait_time = between(0.5, 1)

    def on_start(self):
        # TODO: Login user
        pass

    @task
    def base(self):
        self.client.get("/", name='/')

    @task
    def version(self):
        self.client.get("/v1", name='/v1')

    @task
    def get_classes(self):
        input_mock = {'clinic-id': 1}
        self.client.get("/classes", params=input_mock, name="GET/classes")

    @task
    def put_classes(self):
        input_mock = {'triage-class': {
            'clinic-id': 1,
            'severity': random.randint(1, 5),
            'name': 'Class Name',
            'duration': random.randint(1, 6),
            'proportion': random.uniform(0, 1)
        }}
        self.client.put("/classes", json=input_mock, name="PUT/classes")

    @task
    def predict(self):
        input_mock = {
            'clinic-id': 1,
            'start-date': '2020-02-01',
            'end-date': '2020-02-14',
            'intervals': "[['2020-02-01', '2020-02-14']]"
        }
        self.client.get("/predict", params=input_mock, name='GET/predict')

    @task
    def get_models(self):
        input_mock = {
            'clinic-id': 1
        }
        self.client.get("/models", params=input_mock, name='GET/predict')

    @task
    def set_models(self):
        input_mock = {
            'clinic-id': 1,
            'model-id': 1
        }
        self.client.patch("/models", params=input_mock, name='PATCH/models')

    @task
    def upload_waitlist(self):
        input_mock = {
            'clinic-id': 1
        }
        self.client.put("/upload/waitlist", params=input_mock, name='PUT/upload/waitlist')

    @task
    def upload_historic_data(self):
        input_mock = {
            'clinic-id': 1
        }
        self.client.put("/upload/past-appointments", params=input_mock, name='PUT/upload/past-appointments')
