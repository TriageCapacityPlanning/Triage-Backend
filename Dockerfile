FROM python:3.8
WORKDIR /usr/src/app
COPY ./api/ ./api/
COPY ./sim/ ./sim/
RUN pip install --no-cache-dir -r api/requirements.txt
RUN pip install --no-cache-dir -r sim/requirements.txt
CMD ["python", "-m", "api.triage_api"]