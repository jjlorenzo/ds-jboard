## Stack service commands

```sh
# install deps inside a venv
$ docker-compose run --rm backend-djrf poetry install

# (re-)creates the db and table(s)
$ docker-compose run --rm backend-djrf dropdb --if-exists -hpostgres -Upostgres db-8300
$ docker-compose run --rm backend-djrf createdb --template=template0 -hpostgres -Upostgres db-8300
$ docker-compose run --rm backend-djrf poetry run django-admin.py migrate

# start the backend service with a production server
$ docker-compose up backend-djrf
# this is similar to 
$ docker-compose run --rm --service-ports backend-djrf poetry run jboard --prod server 
# or start the backend service with a development server (aureload)
docker-compose run --rm --service-ports backend-djrf poetry run jboard server
```

## Directory Structure

```sh
├── poetry.lock              # poetry deps lock 
├── poetry.toml              # poetry local config
├── pyproject.toml           # https://python-poetry.org/docs/pyproject/
├── README.md
├── setup.cfg                # only used for configuring `pycodestyle`
├── src
│  └── jboard
│     ├── __init__.py        # package cli entrypoint, for now, only handle `server` command
│     ├── consumers.py       # github jobs api consumer [1]
│     ├── migrations         # django ORM migrations
│     │  ├── 0001_initial.py
│     │  └── __init__.py
│     ├── models.py          # django ORM models definition
│     ├── serializers.py     # drf serializers for req/res validation and serialization [2]
│     ├── settings.py        # django settings
│     ├── urls.py            # url router
│     ├── viewsets.py        # endpoint handlers
│     └── wsgi.py
└── tests
   ├── __init__.py
   └── test_jboard.py

# [1] This is the only python backend where I document the consumer
# [2] Since I don't control the datasource (is from an external api) I feel important to also validate the response
```
