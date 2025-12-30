""""
Simple data generator writes a timestamped .jsonl file with 
200 synthetic records to /data/input.
"""

import json
import os
import random
import datetime
from dateutil import tz

OUT_DIR = "/data/input"
os.makedirs(OUT_DIR, exist_ok=True)

def make_record(i):
    ts = datetime.datetime.utcnow().replace(tzinfo=tz.tzutc()).isoformat()
    return {
        "id": i,
        "timestamp": ts,
        "value": round(random.gauss(50, 15), 3),
        "category": random.choice(["A", "B", "C"])
    }

def main():
    # write a JSONL file 
    fname = os.path.join(OUT_DIR, f"data_{int(datetime.datetime.utcnow().timestamp())}.jsonl")
    with open(fname, "w") as fh:
        for i in range(1, 201): 
            record = make_record(i)
            fh.write(json.dumps(record) + "\n")
    print(f"Generated {fname}")

if __name__ == "__main__":
    main()
