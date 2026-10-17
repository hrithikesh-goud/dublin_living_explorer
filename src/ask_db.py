from pathlib import Path
import sqlite3
import pandas as pd

DB_FILE = Path(__file__).resolve().parent.parent / "data" / "dublin.db"
conn = sqlite3.connect(DB_FILE)

def ask(sql):
    """Send a SQL question to the database and print the answer."""
    print(pd.read_sql_query(sql, conn))
    print("-" * 60)

# # ===== MY QUESTIONS =====

# # Q1: show 5 rows
# ask("SELECT * FROM rent LIMIT 5")

# # Q2: which districts exist?
# ask("SELECT DISTINCT district FROM rent ORDER BY district")

# # Q3: how has Rathmines rent changed over the years?
# ask("""
#     SELECT year, avg_rent
#     FROM rent
#     WHERE area = 'Rathmines'
#       AND bedrooms = 'All bedrooms'
#       AND property_type = 'All property types'
#     ORDER BY year
# """)

# # Q4: The 5 most expensive areas in 2025?
# ask("""
#     SELECT area, avg_rent,district
#     FROM rent
#     WHERE year = 2025 AND area != district AND bedrooms ='All bedrooms' AND property_type = 'All property types'
#     ORDER BY avg_rent DESC
#     LIMIT 5
# """)

# # Q5: The 5 cheapest areas in 2025?
# ask("""
#     SELECT area, avg_rent,district
#     FROM rent
#     WHERE year = 2025 AND area != district AND bedrooms ='All bedrooms' AND property_type = 'All property types'
#     ORDER BY avg_rent ASC
#     LIMIT 5
# """)
# ask("""SELECT area,bedrooms,property_type,year,avg_rent FROM rent
# WHERE year = 2025 AND property_type = 'All property types' AND bedrooms = 'Two bed' AND avg_rent IS NOT NULL AND area != district
# ORDER BY avg_rent 
# LIMIT 5



# """)
# ask("SELECT DISTINCT bedrooms FROM rent")

ask("""
SELECT district,
COUNT(*) AS num_areas,
ROUND(AVG(avg_rent),0) AS district_rent
FROM rent
WHERE year = 2025
AND bedrooms = 'Two bed'
AND property_type = 'All property types'
AND area != district
AND avg_rent IS NOT NULL
GROUP BY district
ORDER BY district_rent
""")

conn.close()
