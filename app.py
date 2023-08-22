import os
from flask import Flask, jsonify
import pandas as pd
from dotenv import load_dotenv

app = Flask(__name__)

# load env varaibles
load_dotenv()

sheet_id = os.environ["SHEET_ID"]
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
records = df.to_dict(orient="records")

@app.route("/")
def welcome():
    return jsonify({"message": "welcome to mentor checklist API!"})

@app.route("/records")
def rows():
    return jsonify({"records": records})


if __name__ == "__main__":
    app.run(debug=True)
