# Triage Backend

## Documentation

You can view the documentation for the various portions of the api by opening the docs in `docs/api/index.html`

## Data Bases w/ Docker
To run the docker container that is already prepared, navigate to this cloned repository and run the following:

```bash
PSQL_LOCAL_PATH="${HOME}/docker/volumes/postgres"
mkdir -p $PSQL_LOCAL_PATH
export TRIAGE_DB_USERNAME="admin"
export TRIAGE_DB_PASSWORD="docker"
export TRIAGE_DB="triage"
docker run --rm --name triage-db -e POSTGRES_PASSWORD=${TRIAGE_DB_PASSWORD} -e POSTGRES_USER=${TRIAGE_DB_USERNAME} -e POSTGRES_DB=${TRIAGE_DB} -d -p 5432:5432 -v ${PSQL_LOCAL_PATH}:/var/lib/postgresql/data postgres:13-alpine 
```

This will run the db in an container named triage-db on port 5432. You can change the path portion of the command (`$HOME/docker/volumes/postgres`) to a local directory to keep the changes you make locally for the next run or omit the -v flag/argument altogether.

In this container, the following are the necessary credential values are set on lines 2-4 of the above commands.

We can connect to the db via the command line with:

```bash
psql -h localhost -U ${TRIAGE_DB_USERNAME} -d ${TRIAGE_DB}
```

Then entering the password in the table above.

The db is nor running on port 5432 with empty tables.

This satisfies the following from the Design Specification:
- [Database Module](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#database-module)

## Triage API
### Usage
To run the API begin by installing the required python dependencies by navigating to the `api` folder and running:

```bash
pip install -r requirements.txt
```

Then run the API locally by running:
```bash
python ./triage_api.py
```

The API will run on localhost (port 5000) by default.

### Endpoints
Currently the following endpoints are implemented:
- [GET /predict](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1predict)
- [GET /classes](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1classes)
- [PUT /classes](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#put-v1classes)
- [GET /models](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#get-v1models)
- [PATCH /models/use](https://github.com/TriageCapacityPlanning/Triage/wiki/Design#patch-v1modelsuse)

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
