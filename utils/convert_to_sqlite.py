import sqlite3
import json
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data_file", help="Path to your data_file")
parser.add_argument("sqlite_file", help="Path to your sqlite_file")
args = parser.parse_args()

conn = sqlite3.connect(args.sqlite_file)
conn.cursor().execute("CREATE TABLE IF NOT EXISTS score (timestamp INTEGER, score INTEGER);")
conn.commit()

f = open(args.data_file,"r")
lines = f.readlines()
f.close()
d = []
for l in lines:
    tmp = json.loads(l.strip())
    ts = datetime.strptime(tmp["date"], "%d.%m.%Y - %H:%M")
    d.append((str(ts), tmp["score"]))

conn.cursor().executemany("INSERT INTO score VALUES (datetime(?),?)",d)
conn.commit()
