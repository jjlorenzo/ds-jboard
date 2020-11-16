## Stack service commands

```sh
# install deps inside a venv
$ docker-compose run --rm backend-connexion poetry install

# (re-)creates the db and table(s)
$ docker-compose run --rm backend-connexion dropdb --if-exists -hpostgres -Upostgres db-8200
$ docker-compose run --rm backend-connexion createdb --template=template0 -hpostgres -Upostgres db-8200
$ docker-compose run --rm backend-connexion poetry run jboard create-tables

# start the backend service with a production server
$ docker-compose up backend-connexion
# this is similar to 
$ docker-compose run --rm --service-ports backend-connexion poetry run jboard --prod server
# or start the backend service with a development server (aureload)
$ docker-compose run --rm --service-ports backend-connexion poetry run jboard server
```

## Directory Structure

```sh
├── poetry.lock              # poetry deps lock 
├── poetry.toml              # poetry local config
├── pyproject.toml           # https://python-poetry.org/docs/pyproject/
├── README.md
├── setup.cfg                # only used for configuring `pycodestyle`
├── src
│   └── jboard
│       ├── __init__.py      # package cli entrypoint, for now, only handle `server` and `create-tables` command
│       ├── consumers.py     # github jobs api consumer [1]
│       ├── models.py        # peewee ORM models definition
│       ├── schemes
│       │   └── v1.yaml      # OpenAPI specification [2]
│       └── viewsets         # endpoint handlers (automatically routed by `connexion.RestyResolver`) [3]
│           └── positions.py
└── tests
    ├── __init__.py
    └── test_jboard.py


# [1] Refer to the `djrf` repository for a commented version of this file
# [2] Connexion automagically handles routing, request parameter validation and response serialization based on this
# [3] My response serialization probably is not the more performant one, but in this project I prefer to have schema
#     validation errors than IndexError, in fact in the future the `_response_keys` should be extracted from the schema
```
