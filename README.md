# Triage Backend

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