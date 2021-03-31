FROM python:3.8
WORKDIR /usr/src/app
COPY ./api/ ./api/
COPY ./sim/ ./sim/
COPY ./uploads/ ./uploads/
RUN apt-get update
RUN apt-get install -y git
RUN cd /opt && \
    git clone https://github.com/TriageCapacityPlanning/Triage-ML-Training.git
RUN cd /opt/Triage-ML-Training/ml-training && \
    pip install .
RUN pip install --no-cache-dir -r api/requirements.txt
RUN pip install --no-cache-dir -r sim/requirements.txt
CMD ["python", "-m", "api.triage_api"]