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
  # cme_unique_id = db.Column(db.BigInteger)
  # drill_unique_id = db.Column(db.Text)
  # essential_cme_topic = db.Column(db.Boolean)
  # essential_drill_topic = db.Column(db.Boolean)
  # facility_code = db.Column(db.Text)
  # facility_name = db.Column(db.Text)
  # id_number_cme = db.Column(db.Text)
  # id_number_drill = db.Column(db.Text)
  mentor_name = db.Column(db.Text)
  # submission_id = db.Column(db.BigInteger)
  success_story = db.Column(db.Text)

@app.route("/")
def welcome():
    return jsonify({"message": "welcome to mentor checklist API!"})


@app.route("/load_data", methods=["POST"])
def load_data():
  sheet_id = os.environ["SHEET_ID"]
  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
  df.fillna("None", inplace=True)
  
  # df['essential_cme_topic'] = df['essential_cme_topic'].fillna(False)
  # df['essential_drill_topic'] = df['essential_drill_topic'].fillna(False)
  # df['drill_unique_id'] = df['drill_unique_id'].fillna('')
  # df['cme_unique_id'] = df['cme_unique_id'].fillna(0)
  # df['id_number_cme'] = df['id_number_cme'].fillna('')
  # df['id_number_drill'] = df['id_number_drill'].fillna('')
  # df['facility_code'] = df['facility_code'].split('-')[0]
  # df['facility_name'] = df['facility_name'].fillna('').split('-')[:]

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
      if row['_id'] != "None":
         submission_id = str(row['_id'])
      else:
         submission_id = None

      entry = MentorChecklist(
        id=index,
        cme_completion_date = cme_completion_date,
        date_submitted = date_submitted,
        success_story=row['mentor_checklist/success_grp/story_success'],
        mentor_name=row['mentor_checklist/mentor/name'],
        county=row['mentor_checklist/mentor/q_county'],
        cme_topic=row['mentor_checklist/cme_grp/cme_topics'],
        drill_topic=row['mentor_checklist/drills_grp/drill_topics'],
        submission_id=submission_id
      )
      db.session.add(entry)
    db.session.commit()
    return "Data loaded successfully!"
  except Exception as e:
     return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
