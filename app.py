import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)

# load env varaibles
load_dotenv()

username=os.environ["DB_USER"]
password=os.environ["DB_PASSWORD"]
db_name=os.environ["DB_NAME"]
db_host=os.environ["DB_HOST"]
db_port=os.environ["DB_PORT"]
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{db_host}:{db_port}/{db_name}"
db = SQLAlchemy(app)

class MentorChecklist(db.Model):
  __tablename__ = 'mentor_checklist'
  id = db.Column(db.BigInteger, primary_key=True)
  cme_completion_date = db.Column(db.Date)
  cme_topic = db.Column(db.Text)
  county = db.Column(db.Text)
  date_submitted = db.Column(db.TIMESTAMP)
  drill_topic = db.Column(db.Text)
  cme_unique_id = db.Column(db.BigInteger)
  drill_unique_id = db.Column(db.Text)
  essential_cme_topic = db.Column(db.Boolean)
  essential_drill_topic = db.Column(db.Boolean)
  facility_code = db.Column(db.Text)
  facility_name = db.Column(db.Text)
  id_number_cme = db.Column(db.Text)
  id_number_drill = db.Column(db.Text)
  mentor_name = db.Column(db.Text)
  submission_id = db.Column(db.BigInteger)
  success_story = db.Column(db.Text)

@app.route("/")
def welcome():
    return jsonify({"message": "welcome to mentor checklist API!"})


@app.route("/load_data", methods=["POST"])
def load_data():
  sheet_id = os.environ["SHEET_ID"]
  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
  df.fillna("None", inplace=True)

  # Insert data into the database
  try:
    for index, row in df.iterrows():
      cme_completion_date = None
      if row["mentor_checklist/cme_grp/cme_completion_date"] != 'None':
         cme_completion_date = datetime.strptime(
            str(row['mentor_checklist/cme_grp/cme_completion_date']), '%Y-%m-%d').date()
      else:
         cme_completion_date = None
      
      date_submitted = None
      if row["_submission_time"] != 'None':
         date_submitted = datetime.strptime(str(row["_submission_time"]), "%Y-%m-%dT%H:%M:%S")
      else:
         date_submitted = None
      
      submission_id = None
      if isinstance(row['_id'], int):
         submission_id = int(row['_id'])
      else:
         submission_id = None
      
      essential_cme_topic = None
      if row['mentor_checklist/cme_grp/cme_topics'] == ("Postpartum_haemorrhage_(PPH)" or "Infection_prevention"):
         essential_cme_topic = True
      else:
         essential_cme_topic = False

      essential_drill_topic = None
      if row['mentor_checklist/drills_grp/drill_topics'] == "Eclampsia":
         essential_drill_topic = True
      else:
         essential_drill_topic = False

      drill_unique_id = None
      if row['mentor_checklist/drills_grp/drill_topics'] == "Eclampsia":
         drill_unique_id = 240331573077017
      else:
         drill_unique_id = None
      
      cme_unique_id = None
      if row['mentor_checklist/cme_grp/cme_topics'] == "Postpartum_haemorrhage_(PPH)":
         cme_unique_id = 372381678562412
      else:
         cme_unique_id = None

      id_number_cme = None
      if row['mentor_checklist/cme_grp/standard_phone_numbers_cme/id_number_1_001'] != 'None':
         id_number_cme = str(row['mentor_checklist/cme_grp/standard_phone_numbers_cme/id_number_1_001'])
      else:
         id_number_cme = None
      
      id_number_drill = None
      if row['mentor_checklist/drills_grp/id_numbers_drill/id_drill_1'] != "None":
         id_number_drill = str(row['mentor_checklist/drills_grp/id_numbers_drill/id_drill_1'])
      else:
         id_number_drill = None
      
      facility_code = None
      facility_name = None
      facility = str(row['mentor_checklist/mentor/q_facility_bungoma'])
      if facility != "None":
         facility_code = facility.split('_')[0]
         facility_name_str = facility.split('_')[1:]
         facility_name = ' '.join(facility_name_str)
      else:
         facility_code = None
         facility_name = None

      entry = MentorChecklist(
        id = index,
        cme_completion_date = cme_completion_date,
        date_submitted = date_submitted,
        essential_cme_topic = essential_cme_topic,
        essential_drill_topic = essential_drill_topic,
        success_story = row['mentor_checklist/success_grp/story_success'],
        mentor_name = row['mentor_checklist/mentor/name'],
        county = row['mentor_checklist/mentor/q_county'],
        cme_topic = row['mentor_checklist/cme_grp/cme_topics'],
        drill_topic = row['mentor_checklist/drills_grp/drill_topics'],
        drill_unique_id = drill_unique_id,
        cme_unique_id = cme_unique_id,
        id_number_cme = id_number_cme,
        id_number_drill = id_number_drill,
        facility_name = facility_name,
        facility_code = facility_code,
        submission_id = submission_id
      )
      db.session.add(entry)
    db.session.commit()
    return "Data loaded successfully!"
  except Exception as e:
     return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
