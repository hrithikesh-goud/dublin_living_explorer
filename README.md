# Dublin Living Explorer

Helps students and new arrivals choose where to live in Dublin by comparing
rent, commute times and transport access across areas.

## Status

Stage 1: complete ✅

## Roadmap

| Stage | What I build | What I learn |
|---|---|---|
| 1. Get the data | Load RTB rent data (from the CSO) into a database and query it | Pandas, SQL, Git |
| 2. Automate | Collect live Dublin Bikes and transport data every 15 minutes | APIs, GitHub Actions, PostgreSQL (Supabase) |
| 3. Analyse | Rent trends, bike usage patterns, weather effects, Power BI dashboard | Window functions, statistics, Power BI |
| 4. App | "Where should I live?" Streamlit app with map, deployed publicly | Streamlit, Folium/Plotly, deployment |
| 5. ML / AI | Bike availability forecast, rent prediction, AI assistant | Scikit-learn, LLM APIs, RAG |
| 6. Full stack | Rebuild as Next.js + FastAPI app | React, Next.js, FastAPI |

## Data sources

- Rent: RTB Rent Index, published by the CSO (PxStat table RIA02, annual)
- Dublin Bikes: live station API (Stage 2)
- Transport: NTA GTFS and GTFS-Realtime (Stage 2)
- Weather: Met Éireann API (Stage 3)

## Getting started

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt

python src/get_rent.py      # 1. download RTB rent data (CSO table RIA02)
python src/clean_rent.py    # 2. keep Dublin, tidy columns  -> data/rent_dublin_clean.csv
python src/load_to_db.py    # 3. load into SQLite           -> data/dublin.db
python src/ask_db.py        # 4. run the SQL questions
```
## Findings

Source: RTB average monthly rent (CSO table RIA02), "All bedrooms" and
"All property types", individual areas only (district totals excluded).

1. **Most expensive area in 2025:** Mount Merrion (Co. Dublin) at **€3,757/month**,
   followed by Foxrock (D18) €3,448 and Goatstown (D14) €3,210.
2. **Cheapest area in 2025:** Cabra (D7) at **€1,606/month**, followed by
   Clonliffe (D3) €1,638 and Rathmines (D6) €1,651.
3. **The gap is large:** renting in Mount Merrion costs **134% more (2.3×)**
   than in Cabra.
4. **Rathmines rent nearly doubled** in 12 years: from €866 (2013) to €1,651 (2025),
   **+91%**. Growth slowed recently: +1.7% from 2024 to 2025.
5. **Averages hide the mix:** Rathmines ranks among the cheapest overall partly because
   it has many small units (bedsits and 1-bed flats). A like-for-like comparison
   by bedroom count is the next step.