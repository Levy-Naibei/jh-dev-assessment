import os
import pandas as pd
from dotenv import load_dotenv

# load env varaibles
load_dotenv()

sheet_id = os.environ["SHEET_ID"]
print(sheet_id)
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
records = df.to_dict(orient="records")

# print(records)
# print(df)
