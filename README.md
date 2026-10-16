# Dublin Living Explorer

Helps students and new arrivals choose where to live in Dublin by comparing
rent, commute times and transport access (Dublin Bus, Luas, DART, Dublin Bikes) across areas.

## Status

✅ **Stage 1 complete:** rent data pipeline (ETL → SQLite → SQL findings)
⏳ **Next:** Stage 2, automating live transport data

## Roadmap

| Stage | What I build | What I learn |
|---|---|---|
| 1. Get the data ✅ | RTB rent data from the CSO API → clean → SQLite → SQL analysis | Python, pandas, ETL, SQL, Git |
| 2. Automate | Live Dublin Bikes, bus, Luas and DART data every 15 minutes, with monitoring and alerts | APIs, GitHub Actions, PostgreSQL |
| 3. Analyse | Rent trends, transport reliability, weather effects; Power BI and Grafana dashboards | Window functions, statistics, BI |
| 4. App | "Where should I live?" Streamlit map app with live transport, deployed publicly | Streamlit, Folium, deployment |
| 5. ML / AI | Rent and bike-availability prediction, AI assistant, MCP server | scikit-learn, LLMs, RAG, agents |
| 6. Full stack | Rebuild as a Next.js + FastAPI app | React, Next.js, FastAPI |

## Pipeline (Stage 1)

```
CSO API ──► get_rent.py ──► clean_rent.py ──► load_to_db.py ──► dublin.db ──► SQL
(337,176 rows)  Extract      Transform           Load          (43,879 Dublin rows)
```

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

## Data sources

- **Rent:** RTB average monthly rent, published by the CSO (PxStat table **RIA02**, annual, 2008–2025)
- **Dublin Bikes:** live station API (Stage 2)
- **Bus, Luas, DART:** NTA GTFS and GTFS-Realtime, Irish Rail API (Stage 2)
- **Weather:** Met Éireann API (Stage 3)

## Findings

Source: RTB average monthly rent, "All bedrooms" and "All property types",
individual areas only (district totals excluded).

1. **Most expensive area in 2025:** Mount Merrion (Co. Dublin) at **€3,757/month**,
   followed by Foxrock (D18) €3,448 and Goatstown (D14) €3,210.
2. **Cheapest area in 2025:** Cabra (D7) at **€1,606/month**, followed by
   Clonliffe (D3) €1,638 and Rathmines (D6) €1,651.
3. **The gap is large:** renting in Mount Merrion costs **134% more (2.3×)** than in Cabra.
4. **Rathmines rent nearly doubled** in 12 years: from €866 (2013) to €1,651 (2025),
   **+91%**. Growth slowed recently: +1.7% from 2024 to 2025.
5. **Averages hide the mix:** Rathmines ranks among the cheapest overall partly because
   it has many small units. A like-for-like comparison by bedroom count is next.

## Data notes

- 66% of RTB values are suppressed (too few tenancies), so they're left missing, not filled in.
- Categories are hierarchical ("All bedrooms" includes "One bed", and districts include
  their areas), so queries pick one level to avoid double counting.
  
  ### Like-for-like comparison: cheapest areas for a 2-bed (2025)

Comparing average rents across areas is misleading when the bedroom mix differs.
With all bedroom types combined, inner-city areas like Rathmines appeared among the
cheapest, because they have many small flats. Comparing **2-beds only** gives a
different picture:

| Area | District | Avg monthly rent (2-bed, 2025) |
|---|---|---|
| Rush | Dublin | €1,551 |
| Ongar | Dublin | €1,672 |
| Balbriggan | Dublin | €1,673 |
| Clonee | Dublin | €1,736 |
| Skerries | Dublin | €1,741 |

**Insight:** the cheapest 2-beds are in outer commuter towns, not the inner city.
Cheap rent alone doesn't make an area a good place to live, so the next stage adds
commute and transport data.

```sql
SELECT area, district, avg_rent
FROM rent
WHERE year = 2025
  AND bedrooms = 'Two bed'
  AND property_type = 'All property types'
  AND area != district
  AND avg_rent IS NOT NULL
ORDER BY avg_rent
LIMIT 5;
```