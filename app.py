import os
from flask import Flask, jsonify
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)

# load env varaibles
load_dotenv()

sheet_id = os.environ["SHEET_ID"]
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
df.fillna("", inplace=True)
# records = df.to_dict(orient="records")


@app.route("/")
def welcome():
    return jsonify({"message": "welcome to mentor checklist API!"})


# @app.route("/records")
# def rows():
#     return jsonify({"records": records})


@app.route("/load_data", methods=["POST"])
def load_data():
    try:
        conn = psycopg2.connect(
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
        )

        cursor = conn.cursor()

        for index, row in df.iterrows():
            cme_completion_date = row.get("cme_completion_date", None)
            if cme_completion_date:
                cme_completion_date = datetime.strptime(
                    cme_completion_date, "%Y-%m-%d"
                ).date()

            date_submitted = row.get("date_submitted", None)
            if date_submitted:
                date_submitted = datetime.strptime(date_submitted, "%Y-%m-%dT%H:%M:%S")

            insert_query = """
            INSERT INTO mentor_checklist (
                cme_completion_date,
                cme_topic,
                cme_unique_id,
                county,
                date_submitted,
                drill_topic,
                drill_unique_id,
                essential_cme_topic,
                essential_drill_topic,
                facility_code,
                facility_name,
                id_number_cme,
                id_number_drill,
                mentor_name,
                submission_id,
                success_story
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            values = (
                cme_completion_date,
                row.get("cme_topic", ""),
                row.get("cme_unique_id", None),
                row.get("county", ""),
                date_submitted,
                row.get("drill_topic", ""),
                row.get("drill_unique_id", ""),
                row.get("essential_cme_topic", False),
                row.get("essential_drill_topic", False),
                row.get("facility_code", ""),
                row.get("facility_name", ""),
                row.get("id_number_cme", ""),
                row.get("id_number_drill", ""),
                row.get("mentor_name", ""),
                row.get("submission_id", None),
                row.get("success_story", ""),
            )
            cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Data uploaded successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
