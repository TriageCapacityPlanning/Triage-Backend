FROM python:3.8
WORKDIR /usr/src/app
COPY . ./api/
RUN pip install --no-cache-dir -r api/requirements.txt
CMD ["python", "-m", "api.triage_api"]