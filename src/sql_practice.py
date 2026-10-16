import sqlite3
import pandas as pd

# 16 rows with the same columns as the real rent table
rows = [
    (2024, "Rathmines",     "Dublin 6",  "All bedrooms", "All property types", 1623),
    (2025, "Rathmines",     "Dublin 6",  "All bedrooms", "All property types", 1651),
    (2025, "Rathmines",     "Dublin 6",  "One bed",      "All property types", 1480),
    (2025, "Rathmines",     "Dublin 6",  "Two bed",      "All property types", 2050),
    (2025, "Ranelagh",      "Dublin 6",  "All bedrooms", "All property types", 2380),
    (2025, "Ranelagh",      "Dublin 6",  "Two bed",      "All property types", 2600),
    (2025, "Dublin 6",      "Dublin 6",  "All bedrooms", "All property types", 2010),
    (2024, "Cabra",         "Dublin 7",  "All bedrooms", "All property types", 1580),
    (2025, "Cabra",         "Dublin 7",  "All bedrooms", "All property types", 1606),
    (2025, "Cabra",         "Dublin 7",  "Two bed",      "All property types", 1750),
    (2025, "Arbour Hill",   "Dublin 7",  "Two bed",      "All property types", None),
    (2025, "Foxrock",       "Dublin 18", "All bedrooms", "All property types", 3448),
    (2025, "Foxrock",       "Dublin 18", "Two bed",      "Apartment",          2900),
    (2025, "Mount Merrion", "Dublin",    "All bedrooms", "All property types", 3757),
    (2025, "Clonliffe",     "Dublin 3",  "All bedrooms", "All property types", 1638),
    (2025, "Clonliffe",     "Dublin 3",  "One bed",      "Apartment",          None),
]

df = pd.DataFrame(rows, columns=["year", "area", "district", "bedrooms", "property_type", "avg_rent"])

conn = sqlite3.connect(":memory:")          # a temporary database in RAM only
df.to_sql("rent", conn, index=False)        # save the DataFrame as a table called rent

def ask(sql):
    print(pd.read_sql(sql, conn).to_string(index=False))
    print()

# ---- write your practice queries below ----
ask("""
    SELECT area,bedrooms,avg_rent FROM rent
    WHERE year = 2025 AND bedrooms = 'Two bed' AND avg_rent IS NOT NULL
    ORDER by avg_rent
    LIMIT 5
    
    
    
    
    """)


conn.close()