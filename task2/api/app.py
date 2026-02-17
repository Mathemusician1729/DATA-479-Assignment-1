""""
API service to provide data summaries from SQLite database
"""
# --------------Imports-------------------
import os
import sqlite3
from flask import Flask, jsonify
import pandas as pd
# ---------------------------------

DB_PATH = os.environ.get("DB_PATH", "/data/db/data.db")
app = Flask(__name__)

def get_conn():
    if not os.path.exists(DB_PATH):
        return None
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@app.route("/")
def index():
    return {"message": "API running. Test endpoints: /summary, /count, /recent"}

@app.route("/summary")
def summary():
    conn = get_conn()
    if conn is None:
        return jsonify({"error":"DB not found", "db_path": DB_PATH}), 404
    df = pd.read_sql_query("SELECT category, COUNT(*) as cnt, AVG(value) as avg_value FROM records GROUP BY category", conn)
    data = df.to_dict(orient="records")
    return jsonify({"summary": data})

@app.route("/count")
def count():
    conn = get_conn()
    if conn is None:
        return jsonify({"count": 0})
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM records")
    cnt = cur.fetchone()[0]
    return jsonify({"count": cnt})

@app.route("/recent")
def recent():
    conn = get_conn()
    if conn is None:
        return jsonify({"rows": []})
    df = pd.read_sql_query("SELECT * FROM records ORDER BY timestamp DESC LIMIT 10", conn)
    print(df.iloc[0])
    print(type(df.iloc[0]["id"]))
    return jsonify({"rows": df.to_dict(orient="records")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
