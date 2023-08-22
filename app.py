import os
from flask import Flask, jsonify
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv

app = Flask(__name__)

# load env varaibles
load_dotenv()

sheet_id = os.environ["SHEET_ID"]
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
df.replace(np.nan, "", inplace=True)
records = df.to_dict(orient="records")


@app.route("/")
def welcome():
    return jsonify({"message": "welcome to mentor checklist API!"})


@app.route("/records")
def rows():
    return jsonify({"records": records})


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

  except Exception as e:
      return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
