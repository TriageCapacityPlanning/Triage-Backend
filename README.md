# Triage Backend

## Data Bases w/ Docker
To run the docker container that is already prepared, navigate to this cloned repository and run the following:

```bash
docker load < data/docker-images/triage-db-empty.tar
docker run --rm --name pg-docker-triage -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data triage-db-empty
```

This will run the db in an image named pg-docker-triage on port 5432. You can change the path portion of the command (`$HOME/docker/volumes/postgres`) to a local directory to keep the changes you make locally for the next run or omit the -v flag/argument altogether.

In this container, the following are the saved values:

| Attribute     | Value         |
| ------------- |:-------------:|
| username      | admin         |
| password      | docker        |
| database      | triage        |

We can connect to the db via the command line with:

```bash
psql -h localhost -U admin -d triage
```

Then entering the password in the table above.

The db is nor running on port 5432 with empty tables.