from pathlib import Path
import sqlite3
import pandas as pd

# JOB 1: find the notebook (CSV) and where the library (database) will go
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_FILE = PROJECT_ROOT / "data" / "rent_dublin_clean.csv"
DB_FILE = PROJECT_ROOT / "data" / "dublin.db"

# JOB 2: read the notebook into Python
df = pd.read_csv(CLEAN_FILE)
print("Rows in CSV:", len(df))

# JOB 3: copy it into the library as a table called "rent"
conn = sqlite3.connect(DB_FILE)          # open the library (creates the file if new)
df.to_sql("rent", conn, if_exists="replace", index=False)

# JOB 4: check, by asking the library how many rows it has
check = pd.read_sql_query("SELECT COUNT(*) AS n FROM rent", conn)
print("Rows in database:", check["n"][0])

conn.close()                             # close the library
print("Done! Saved to:", DB_FILE)