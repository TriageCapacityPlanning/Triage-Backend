# Triage Backend

## Documentation

You can view the documentation for the various portions of the api by opening the docs in `docs/api/index.html`

### Generating Updated Documentation

To generate updated documentation, the pdoc package is required. It can be installed by executing:

```bash
pip install pdoc3
```

To generate the docs, from the root of the repository run the following commands:

```bash
rm -r docs/api # Remove the previous docs
pdoc --html --output-dir docs api # Generate the api documentation into the docs folder
```

Note: This requires a local installation of the Triage-ML-Training python module. Follow the instructions [here](https://github.com/TriageCapacityPlanning/Triage-ML-Training#local-installation-not-recommended) to do so.

## Usage

### Backend Docker Container (Recommended)
To run the entire backend, it is recommended to deploy all modules in docker containers. To do so, run the following command in the root directory of the repository:
```bash
docker-compose up
```

### Run API Locally (Not recommended)
To run the API begin by installing the required python dependencies by navigating to the `api` folder and running:

```bash
pip install -r requirements.txt
```

Then run the API locally by running:
```bash
python ./triage_api.py
```

The API will run on localhost (port 5000) by default.

Note: This requires a local installation of the Triage-ML-Training python module. Follow the instructions [here](https://github.com/TriageCapacityPlanning/Triage-ML-Training#local-installation-not-recommended) to do so.
Note: This also requires the DB docker container from above to be running. This will also require the `host` value in `api/common/config.py` to be set to `localhost`.

## Triage API

### Endpoints
Currently the following endpoints are implemented:
- [GET /auth/login](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1predict)
- [GET /predict](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1predict)
- [GET /classes](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1classes)
- [PUT /classes](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#put-v1classes)
- [GET /models](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1models)
- [PATCH /models/use](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#patch-v1modelsuse)
- [PUT /upload/past-appointments](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1models)
- [POST /upload/model](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1models)
- [GET /data/(clinic-id)/(triage-class)](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#patch-v1modelsuse)

### Unit Testing
To install the requirements for testing by navigating to the `api` folder and running:

```bash
pip install -r requirements.txt
pip install -r test-requirements.txt 
```

The template code for unit testing is currently in the `api/tests/` directory. Unit testing is done through pytest and can be run by simply running the command:
```bash
pytest
```


## Simulation Module

A module that given a series of arrivals, generates a schedule or analyzes a schedule via simulation.

See the module's [README](./sim/README.md) for more developer detail, and [docs/sim](./docs/sim) for design specs.

### Interface

#### sim.gen_min_interval_slots()

Get the minimized schedule in which all interval slots are equal.

See [design details](./docs/sim/minintervalschedule.md) for more info.

See implementation and interface in the [source code](./sim/resources/minintervalschedule.py)

#### sim.simulate_allocations()

Simulate the proposed schedule and return the processing results of each arrival.

See implementation and interface in the [source code](./sim/resources/simulateallocations.py)
