""""
Data loading step, loads processed CSVs from /data/processed into SQLite database /data/db
"""

# --------------Imports-------------------
import os
import glob
import sqlite3
import pandas as pd
# ---------------------------------

PROCESSED_DIR = "/data/processed"
DB_DIR = "/data/db"
DB_PATH = os.path.join(DB_DIR, "data.db")
os.makedirs(DB_DIR, exist_ok=True)

TABLE_NAME = "records"

def init_db(conn):
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER,
        timestamp TEXT,
        value REAL,
        category TEXT,
        value_norm REAL,
        hour INTEGER
    );
    """)
    conn.commit()

def load_csv_to_db(csv_path, conn):
    df = pd.read_csv(csv_path)

    expected = ['id','timestamp','value','category','value_norm','hour']
    for c in expected:
        if c not in df.columns:
            df[c] = None
    records = df[expected].to_records(index=False)
    conn.execute("BEGIN")
    conn.executemany(f"INSERT INTO {TABLE_NAME} (id,timestamp,value,category,value_norm,hour) VALUES (?,?,?,?,?,?)", records)
    conn.commit()
    print(f"Inserted {len(df)} rows from {csv_path}")

def main():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)
    # process all of the processed CSVs
    csvs = sorted(glob.glob(os.path.join(PROCESSED_DIR, "*_processed.csv")))
    if not csvs:
        print("No processed CSVs found.")
        return
    for csv in csvs:
        load_csv_to_db(csv, conn)
    # show count
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total = cur.fetchone()[0]
    print(f"Total rows in table '{TABLE_NAME}': {total}")
    conn.close()

if __name__ == "__main__":
    main()
