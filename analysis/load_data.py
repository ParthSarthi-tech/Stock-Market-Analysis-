import os
import glob
import sqlite3
import pandas as pd

# Resolve base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "market.db")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Find CSV files
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in data folder")

all_data = []

for file in csv_files:
    symbol = os.path.basename(file).replace(".csv", "")
    df = pd.read_csv(file)

    df["symbol"] = symbol
    df["sector"] = "UNKNOWN"

    df.columns = [c.lower() for c in df.columns]
    all_data.append(df)

# Combine all stock data
stocks_df = pd.concat(all_data, ignore_index=True)

# Load into SQLite
stocks_df.to_sql("stocks", conn, if_exists="replace", index=False)

conn.close()

print("✅ Data loaded into SQLite successfully.")
