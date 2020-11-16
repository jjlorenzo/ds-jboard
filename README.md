## Take home project and code review

1. We are building a jobs board website. We will be displaying developer jobs for several cities around the world
2. The user should be able to select a city from this list (Chicago, San Francisco, Phoenix, London, Beijing, Paris)
3. The user should be able to select a job description from this list (Javascript, Java, Python, React, Ruby, Go)
4. When the user selects a city or selects a job description the list of jobs should update to match the user's selections
5. There should be a frontend and a backend. The frontend should communicate to the backend via a REST API
6. The backend should fetch the jobs from Github's public jobs API (eg. [jobs.github.com](https://jobs.github.com/positions?description=javascript&location=san+francisco))
7. The backend should have a database. The database should have one table called `searches` which stores a record of each job search. The `searches` table columns should include time, description, location and ip address of the user.
8. You may use any languages and frameworks that you like

## Remarks from requirements

Since this is home project for code review purpose and the task is simpler enough I'll provide several implementations with different languages and frameworks (8). 

Contrary to Github's Jobs own website, our solution restricts the values for `location`(**#2**) and `description`(**#3**) to a fixed set of values, so we will be using `select` controls instead of regular `input`, also (**#4**) confirms that **user selection** is  what triggers the search action instead of **user text input**.

Since the backend is the one that performs the fetch from Github's public jobs API (**#6**), the frontend only needs to communicate with the backend (**#5**).

Any database backend should work (**#7**) but I'll choose Postgres, the `Search` table will looks like:

|  id  | description | location      | search_at                     | search_from*  |
| :--: | ----------- | ------------- | ----------------------------- | ------------- |
|  1   | Javascript  | Chicago       | 2020-10-31 10:11:12.000013-05 | 173.44.36.186 |
|  2   | Java        | San Francisco | 2020-10-31 11:12:13.000014-05 | 173.44.36.186 |
|  3   | Python      | Phoenix       | 2020-10-31 12:13:14.000015-05 | 173.44.36.186 |
|  4   | React       | London        | 2020-10-31 13:14:15.000016-05 | 173.44.36.186 |
|  5   | Ruby        | Beijing       | 2020-10-31 14:25:16.000017-05 | 173.44.36.186 |
|  6   | Go          | Paris         | 2020-10-31 15:26:17.000018-05 | 173.44.36.186 |

(*) when we use `peewee` ORM, the `IPField` stores the value as bigint.

## Solution

I'm using `alpine:edge` as the base image for the docker container, at least under MacOS there is a bug regarding dns resolution, this is the workaround I use:

```json
# ~/.docker/daemon.json
{
	"dns":["1.1.1.1"],  # this is the only change required, the others are for convenience only
	"experimental":true,
	"features":{"buildkit":true}
}
```

Due to lack of free time, I have delived only **two** different backends and **one** frontend. Both backend behave similar but only the `connexion` based delivers a complete `openapi.json` schema required by the frontend. I use the schema to populate the list of valid values for the `description` and `location` values.

### Backends

#### [Amber](https://amberframework.org/) `crystal` 

The main motivation is that I like very much the `crystal` languaje and this framework is flexible, performant and simpler.

Status: **TODO**

#### [Connexion](https://connexion.readthedocs.io/) `python`

The main strength of this implementation is that is driven by the schema, so it force you to start from the schema, providing a full description of the API from the begining.

I was tempted to use `SQLAlchemy` for the ORM, but `Peewee` is seam a better fit for what it was required. The communication with the github API was implemented with `uplink`. In general I like very much this implementation. Connexion automatically validates the request and response, but I would like that by default it also provide a mechanism to instrospect the schema before returning the response, so I can use only the valid fields to generate the response.

Status: **DONE**

#### [Django REST framework](https://www.django-rest-framework.org/) `python`

This implementation is as much simpler as possible taking into account that is on top of Django and DRF, I explicitly avoid the DRF filtering mechanism and instead use Serializers for both request and response validation/serialization. This backend also provides and `openapi.json` schema but is not completed because the use of Serializers instead of filtering.

Another characteristic os this backend is that I explicitly ignore the `location` filter, so the amount of results can be bigger than `50` and can be used for testing the frontend(s) pagination. Further details of this are documented in the `src/djrf/jboard/src/jboard/consumers.py` file.

Status: **DONE**

#### [LoopBack](https://loopback.io/) `nodejs`

I had good times with this framework in the past, but the current version (4) looks much more complicated and rely much more in generated code, something not good for an exam, so I dely its implementation for now.

Status: **TODO**

#### [Lucky](https://luckyframework.org/) `crystal`

I dely its implementation basically because of the same reasons, its a framework much more like rails where you get a lot of code and conventions from the start and looks complex for this app.

Status: **TODO**

#### [Sails](https://sailsjs.com/) `nodejs`

I was expecting to get my hands on this to remember old times, but I had the same impression that I will probably spend more times removing unused code than adding.

Status: **TODO**

### Frontends

#### [Angular Material](https://material.angular.io/) `angular`

Lack of time, no further complains about this framework, except that Angular in general doesn't look to attractive anymore.

Status: **TODO**

#### [Atlaskit](https://atlaskit.atlassian.com/) `react`

Delayed because my React experience is limited to small previous projects and to the port I'm doing in my (almost inexistent) free time of this library to Vue3.

Status: **TODO**

#### [Atlassian User Interface](https://aui.atlassian.com/aui/9.1.4/) `vue`

The main motivation is that in the past month I had an small project that use this framework, In my case I only use the CSS parts and for the two UI components, I add simpler Vue wrappers. The main motivation was to use the Composition API.

The has the backend selection, for the purpose of testing, something that it won't be delivered if this was a real app, but IMHO good for an exam and testing.

Status: **DONE**

#### [Bootstrap Vue](https://bootstrap-vue.org/) `vue`

Delayed because they don't support Vue3 and using the composition api plugin don't motivate enough, so I will do this later.

Status: **TODO**

#### [PrimeVue](https://www.primefaces.org/primevue) `vue`

Lack of time, it supports Vue 3.X, but in general I didn't see a big benefit for starting with this.

Status: **TODO**

#### [Quasar](https://quasar.dev/) `vue`

They are in the process of supporting Vue3 yet, so I didn't feel attracted to face early bugs.

Status: **TODO**

#### [Vuetify](https://vuetifyjs.com/) `vue`

They are in the process of supporting Vue3 yet, so I didn't feel attracted to face early bugs.

Status: **TODO**

## TLDR

For local development or testing, you need:

- docker and docker-compose
- [crun](https://github.com/Val/crun) for the `reset-stack.cr ` script (or inspecte the file and manually execute the shell commands)

```shell
# example (there are options avaiable with ./reset-stack.cr --help)

$ ./reset-stack.cr
[+] ["docker", "build", "--tag=dstreet/jboard", "."]
...
[+] ["docker-compose", "down", "--remove-orphans", "--volumes"]
...
[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-conn", "poetry", "install"]
...
[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-djrf", "poetry", "install"]
...
[+] ["docker-compose", "run", "--rm", "--no-deps", "frn-vaui", "yarn", "install"]
...
[+] ["docker-compose", "run", "--rm", "--no-deps", "frn-vaui", "yarn", "build"]
...
[+] ["docker-compose", "run", "--rm", "--no-deps", "--name=postgres", "--service-ports", "postgres", "postgres-server.crun", "--log-connections"]
	...
	[+] ["docker-compose", "run", "--rm", "postgres", "pg_isready", "-hpostgres", "-Upostgres"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-conn", "dropdb", "-hpostgres", "-Upostgres", "--if-exists", "db-8200"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-conn", "createdb", "-hpostgres", "-Upostgres", "--template=template0", "db-8200"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-conn", "poetry", "run", "jboard", "create-tables"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-conn", "psql", "-hpostgres", "-Upostgres", "-ddb-8200", "-c\\dt"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-djrf", "dropdb", "-hpostgres", "-Upostgres", "--if-exists", "db-8300"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-djrf", "createdb", "-hpostgres", "-Upostgres", "--template=template0", "db-8300"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-djrf", "poetry", "run", "django-admin.py", "migrate"]
	...
	[+] ["docker-compose", "run", "--rm", "--no-deps", "bck-djrf", "psql", "-hpostgres", "-Upostgres", "-ddb-8300", "-c\\dt"]
	...
[+] ["docker-compose", "up", "--no-deps", "postgres", "bck-conn", "bck-djrf", "frn-vaui"]
...
```



I understand that this instructions are not complete 100%, I can explain more if required.

