""""
Data transformation step, processes all .jsonl files in /data/input, 
creates processed CSV + summary CSV in /data/processed
"""
# --------------Imports-------------------
import os
import glob
import json
import pandas as pd
from datetime import datetime
# ---------------------------------

INPUT_DIR = "/data/input"
PROCESSED_DIR = "/data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def process_file(path):
    # Read JSONL into DataFrame
    rows = []
    with open(path, "r") as fh:
        for line in fh:
            rows.append(json.loads(line))
    if not rows:
        return None
    df = pd.DataFrame(rows)

    # convert timestamp to datetime and extract hour
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour

    # data cleansing: drop NaNs, bound values
    df = df.dropna(subset=['value'])
    df['value'] = df['value'].clip(lower=0)

    # normalize value to 0..1 based on min/max
    vmin = df['value'].min()
    vmax = df['value'].max()
    if vmax > vmin:
        df['value_norm'] = (df['value'] - vmin) / (vmax - vmin)
    else:
        df['value_norm'] = 0.0

    # aggregate summary by category
    summary = df.groupby('category')['value'].agg(['count','mean','min','max']).reset_index()

    # write processed CSV and summary CSV
    base = os.path.basename(path).replace('.jsonl','')
    out_csv = os.path.join(PROCESSED_DIR, f"{base}_processed.csv")
    sum_csv = os.path.join(PROCESSED_DIR, f"{base}_summary.csv")
    df.to_csv(out_csv, index=False)
    summary.to_csv(sum_csv, index=False)
    print(f"Processed {path} -> {out_csv}, {sum_csv}")
    return out_csv

def main():
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.jsonl")))
    if not files:
        print("No input files found.")
        return
    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
