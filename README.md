## Flask API

- This API pulls data from the mentor checklist google
submission sheet, processes it, and loads it into the DB by transforming the
given dataset to fit into the given PostgreSQL table structure.

## Getting started

- clone the repo: `git clone https://github.com/Levy-Naibei/jh-dev-assessment.git`
- `cd jh-dev-assessment`
- run `pip install -r requirements.txt`
- add sheet_id environment variable as shown in `.env.sample.txt`
- run `python app.py`
- interact with api endpoint using `postman`
