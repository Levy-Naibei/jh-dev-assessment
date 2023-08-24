## Flask API

- This API pulls data from the mentor checklist google
submission sheet, processes it, and loads it into the DB by transforming the
given dataset to fit into the given PostgreSQL table structure.

## Prerequisite

- [Docker](https://docs.docker.com/get-docker/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Tools used

- Docker
- Python Flask
- SQLAlchemy ORM
- Google Cloud Platform

## Getting started(Non Docker Environment)

- clone the repo: `git clone https://github.com/Levy-Naibei/jh-dev-assessment.git`
- `cd jh-dev-assessment`
- activate virtual environment: `source venv\bin\activate`
- run `pip install -r requirements.txt`
- add environment variable as shown in `.env.sample.txt`
- run `python app.py`
- interact with api endpoint using `postman` or `curl`

## Getting started (Docker Environment)

- clone the repo: `git clone https://github.com/Levy-Naibei/jh-dev-assessment.git`
- `cd jh-dev-assessment`
- build the docker image: `docker build -t mentor-checklist-api . `
- run `docker run -d -p 4000:5000 mentor-checklist-api`
- Access the api: `http://localhost:4000`

## Allow docker container to connect to a local host postgres database

- use `host ip` not `localhost` to connect to the PostgreSQL database on your host
- cd in configs files:
    - Update `postgresql.conf` by changing from `listen_addresses ='localhost'` to `listen_addresses= '*'`
- Restart PostgresQL:
    - `sudo service postgresql restart` on Linux
    - `brew services restart postgresql` on Mac

## Endpoints

HTTP METHOD | ENV  | Endpoint
------- | ---- | -------------
POST | | `curl --location --request POST 'http://127.0.0.1:5000/load_data'` 
GET |  | `curl --location 'http://127.0.0.1:5000'`
