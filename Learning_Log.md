# Dublin Living Explorer: Learning Log

How to use this file: ⭐⭐⭐ = must know (asked in almost every interview), ⭐⭐ = likely asked, ⭐ = good to know.
Read the questions out loud and answer without looking. Then rewrite each answer in your own words.

---

## Stage 0: Project setup (12 Oct 2026)

### The 30-second pitch ⭐⭐⭐
> "Dublin Living Explorer helps students and new arrivals choose where to live in Dublin. It combines official rent data from the RTB/CSO with transport and bike data, ranks areas by affordability and commute, and shows them on a map. I'm building it in stages: data pipeline → automation → analysis → app → ML/AI → full-stack."

### Key ideas: remember these 5 things

| # | Concept | One-line meaning | Priority |
|---|---|---|---|
| 1 | **Virtual environment (venv)** | A private Python for one project, so libraries don't clash between projects | ⭐⭐⭐ |
| 2 | **requirements.txt** | The list of libraries; makes the setup reproducible with one command | ⭐⭐⭐ |
| 3 | **.gitignore** | Stops `.venv`, big data files and secrets from being uploaded to GitHub | ⭐⭐⭐ |
| 4 | **Project structure** | `src` = code, `sql` = queries, `data` = raw files, `README` = front page | ⭐⭐ |
| 5 | **pip vs venv** | pip installs packages; the venv decides *where* they go | ⭐ |

### Commands I ran (and why)

| Command | What it does | Why |
|---|---|---|
| `python -m venv .venv` | Creates the private environment | Isolation: my ML CA, churn and Dublin projects need different libraries |
| `.venv\Scripts\activate` | Switches the terminal to that environment, so `(.venv)` appears | Otherwise pip installs into the global Python. Needed in every new terminal. |
| `pip install -r requirements.txt` | Installs every library in the file | Reproducible: same setup on any laptop or server |

### Interview questions

**⭐⭐⭐ Q1. What is a virtual environment and why did you use one?**
An isolated Python environment for one project. I have several projects with different dependencies, so a venv stops version clashes. It also makes deployment predictable, because the server installs only what this project needs.

**⭐⭐⭐ Q2. How would someone else run your project?**
Clone the repo → create and activate a venv → `pip install -r requirements.txt` → run the scripts. It's documented in the README's Getting Started section.

**⭐⭐⭐ Q3. What does your .gitignore exclude, and why?**
The `.venv` folder (large, machine-specific, rebuildable from requirements.txt), cache files, large raw data, and above all secrets like API keys and database passwords. Secrets must never go on GitHub.

**⭐⭐ Q4. Walk me through your project structure.**
Standard Python layout: `src` for code, `sql` for queries, `data` for raw downloads, plus README, requirements.txt and .gitignore. Separating code, queries and data makes it easy to navigate, test and deploy.

**⭐⭐ Q5. Why `pandas>=2.0` and not an exact version?**
`>=2.0` gives me bug fixes while guaranteeing pandas 2 features. In production I'd pin exact versions (e.g. `pandas==2.2.3`) or use a lock file for fully repeatable builds. It's a trade-off: flexibility vs stability.

**⭐ Q6. Difference between pip and a venv?**
pip installs packages; the venv is where they get installed. With the venv active, pip installs into the project, not the system Python.

**⭐⭐ Q7. Why is the folder called `.venv`?**
It's the standard name. The dot shows it's a tool folder, not my code. VS Code detects it automatically, and it's in `.gitignore`, so it's never uploaded to GitHub. Anyone can rebuild it from requirements.txt.

**⭐⭐ Q8. How do you know the virtual environment is active?**
The prompt shows `(.venv)` at the start. On Windows, `where python` points inside the project's `.venv` folder. I activate it once in every new terminal.

**⭐⭐⭐ Q9. What is pandas and why did you use it?**
pandas is Python's main library for working with tables of data (DataFrames). I use it to download the CSO rent data, clean it, filter it to Dublin areas, and save it to CSV or a database.

**⭐⭐ Q10. What's a dependency?**
A library that another library needs. pandas depends on numpy, so pip installed numpy, python-dateutil, six and tzdata automatically. That's why pinning versions matters: one upgrade can change things down the chain.

**⭐⭐ Q11. Your requirements say pandas>=2.0 but pip installed 3.0.6. Is that a problem?**
No. `>=2.0` allows anything from 2.0 up, so pip took the newest. A major version jump can change behaviour, so once everything works I'll run `pip freeze > requirements.txt` to lock the exact versions I tested.

**⭐ Q12. How do you check what's installed?**
`pip list` shows everything in the active environment. `pip freeze > requirements.txt` saves the exact versions.

### What got installed
pandas 3.0.6, numpy 2.5.4, python-dateutil 2.9.0, six 1.17.0, tzdata 2026.5

### Mistakes I hit (interviewers love these stories)
- Created the `data` folder in the wrong place (Desktop) because the terminal was in a different folder. **Lesson:** always check the path in the prompt before running commands.
- Opened files inside a zip instead of the extracted folder. **Lesson:** extract first, and work only in real folders.
- Typed `Y` on its own in the terminal and got a red error. There was no question waiting, so PowerShell treated "Y" as a command. **Lesson:** read red errors calmly. Often they're harmless.

---

## Stage 1: Rent data (12–13 Oct 2026, in progress)

### What I built
- `src/get_rent.py`: downloads RTB rent data (CSO table **RIA02**, annual) using `requests`, fixes encoding, saves `data/rent_annual_raw.csv`
- `src/explore_rent.py`: explores years, categories, missing values and Dublin locations
- Added `requests>=2.31` to requirements.txt; set the VS Code interpreter to `.venv`

### The data (know these numbers!) ⭐⭐⭐
- **337,176 rows × 12 columns**, all of Ireland, **2008–2025** (18 years)
- One row = average monthly rent for one **area × year × bedrooms × property type**
- 7 bedroom options, 6 property types, 446 locations: a full grid (18×7×6×446 = 337,176)
- **66% missing** (223,497 rows): the RTB hides averages based on too few tenancies
- **167 Dublin locations**, named "Area, Dublin 7" (postal district) or "Area, Dublin" (county)
- Each category comes as a **code + label** pair; keep Year, Number of Bedrooms, Property Type, Location, VALUE

### Interview questions

**⭐⭐⭐ Q1. Where does your rent data come from?**
The Residential Tenancies Board rent index, published by the CSO through their PxStat API (table RIA02). Average monthly rent by area, year, property type and bedrooms. It's official data from registered tenancies: rents actually paid, not advertised asking prices.

**⭐⭐⭐ Q2. Why use an API instead of downloading manually?**
It's reproducible and automatable. Anyone can rerun the script to get the latest data, and in Stage 2 I'll schedule it with GitHub Actions.

**⭐⭐⭐ Q3. Tell me about a problem you hit (the 403 story).**
The CSO API returned 403 Forbidden. I assumed the server was blocking Python, so I added a User-Agent and then full browser headers, but it still failed. When I printed the response body, I saw the browser had been getting the same error. So my assumption was wrong. I checked the official open-data portal (data.gov.ie) and found the quarterly table RIQ02 was no longer listed. I switched to the annual table RIA02 (updated May 2026), and it worked. **Lesson: read the actual error and verify the source before guessing the cause.**

**⭐⭐ Q4. HTTP status codes?**
200 OK · 403 Forbidden (understood but refused) · 404 Not Found (wrong URL) · 500 Server error.

**⭐⭐ Q5. Why use `requests` instead of `pd.read_csv(url)`?**
Control: headers, a timeout, status-code checks (`raise_for_status`), error handling, and later retries and logging for automation.

**⭐⭐ Q6. Why annual data, not quarterly?**
The quarterly table was unavailable. Annual is enough for comparing areas and long-term trends; the trade-off is less detail on short-term changes.

**⭐⭐ Q7. Why save a raw copy before cleaning?**
It separates extract from transform (the E and T in ETL). If cleaning has a bug, I rerun from the raw file without calling the API again. It's also an audit trail.

**⭐⭐ Q8. Why pathlib + `__file__` for paths?**
The path is built from the script's own location, so it works whichever folder you run it from, and on any OS.

**⭐⭐ Q9. What is a BOM?**
Byte Order Mark: invisible bytes at the start of some UTF-8 files. Decoded wrongly, they show as `ï»¿` and corrupt the first column name. Fix: decode with `utf-8-sig`.

**⭐⭐ Q10. Why read everything as text first (`dtype=str`)?**
It's defensive: type-guessing can silently corrupt values or create mixed types. I read as text, then explicitly convert what I need (`pd.to_numeric(..., errors="coerce")`, where unparseable values become NaN).

**⭐⭐⭐ Q11. What's the first thing you do with a new dataset?**
Explore before cleaning: size, types, date range, unique values per category (`value_counts`), and missing values, so my cleaning is based on facts, not assumptions.

**⭐⭐⭐ Q12. You have 66% missing values. What did you do?**
I found out why first: the RTB suppresses small samples, so the gaps aren't random. Filling them with averages would invent rents that don't exist. I keep them missing, report coverage, and use the most aggregated level ("All bedrooms" + "All property types") for each area. The app shows "insufficient data" instead of a fake number.

**⭐⭐⭐ Q13. What's a common mistake with this data?**
Double counting. The categories are hierarchical ("All bedrooms" includes "One bed", "Two bed", and so on), so summing across all rows counts the same tenancies several times. Pick one level.

**⭐⭐ Q14. How did you check the structure?**
`value_counts` showed identical counts in every category, so it's a full grid, confirmed by 18 × 7 × 6 × 446 = 337,176.

**⭐⭐ Q15. Why separate scripts (get / explore / clean)?**
Single responsibility: each is short and testable, I can rerun the analysis without hitting the API, and it mirrors a real ETL pipeline.

**⭐⭐ Q16. Terminal Python vs VS Code interpreter?**
They're separate settings. Point both at `.venv`, otherwise the editor shows false errors and ▶ runs the wrong Python.

**⭐ Q17. Why does pandas show `...`?**
Hidden columns on a wide table. Use `df.columns` or `pd.set_option('display.max_columns', None)`.

**⭐ Q18. Script ran but printed nothing?**
Check it's the right file, saved, and in the right folder (an unsaved file runs as its old version). Add a print at the top to confirm the code runs.

### Mistakes I hit (and lessons)
- Ran with the ▶ button → wrong Python and wrong folder. **Always run from the activated `.venv` terminal.**
- Assumed "bot blocking" without reading the error body. **Read the actual response first.**
- Used a table code without verifying it on the official portal. **Verify the source before writing code.**
- Deleted a line but forgot to paste its replacement → "df is not defined". **Check the Problems panel before running.**
- Ran an unsaved file (● on the tab) → no output. **Turned on Auto Save.**

### Next step
`src/clean_rent.py`: keep the useful columns → filter to Dublin → split "Area, Dublin 7" into area + district → save `data/rent_dublin_clean.csv`.
## Stage 1c: Like-for-like rent comparison (16 Oct 2026)

### What I did
- Checked the real database structure before querying: `PRAGMA table_info(rent)` (columns) and `SELECT DISTINCT bedrooms` (exact values)
- Found the real 2-bed label is `'Two bed'` (a guess of `'Two'` would have returned 0 rows with no error)
- Wrote the 2-bed cheapest-areas query myself; result: Rush, Ongar, Balbriggan, Clonee, Skerries

### Mistakes and lessons
- `ORDER BY area` sorts alphabetically, not by price → sort by `avg_rent`
- Forgot to `SELECT avg_rent` → couldn't check the order; always show the sort column
- Ran an unsaved file 3 times (● on the tab) → turned on Auto Save
- VS Code had the outer folder open → new terminals started in the wrong place
- `ask_db.py` runs every query in the file → comment out old ones with Ctrl + /

### Interview Q&A
- ⭐⭐⭐ **How do you start with a database you haven't seen?** Check tables and columns (`PRAGMA table_info` / `information_schema`), then real values with `SELECT DISTINCT`. Wrong text values don't error, they return nothing.
- ⭐⭐⭐ **What did like-for-like change?** All-bedroom averages made Rathmines look cheap (many small flats). 2-beds only: outer commuter towns are cheapest (Rush ~€1,551). Rent alone is misleading, so the app adds commute data.
- ⭐⭐ **Can you ORDER BY a column you don't SELECT?** Yes, but better to show it so results can be checked.
- ⭐ **Code change had no effect?** Check the file is saved and you're in the right folder and interpreter.

## Stage 1d: District summary with GROUP BY (17 Oct 2026) ✅ Stage 1 complete

### What I did
- Built the district query in 4 parts: WHERE (88 rows) → GROUP BY + AVG → COUNT/ROUND/AS → ORDER BY
- Result: Dublin 15 cheapest reliable district (€1,888, 8 areas); Dublin 4 most expensive (€2,432)

### Mistakes and lessons
- Commented out the setup lines (imports, conn, def ask) → NameError: 'ask' is not defined
- Uncommenting left a space before a top-level line → IndentationError
- Typed `python /src.ask_db.py` → use `python src/ask_db.py` (↑ key to reuse commands)
- Lost WHERE + GROUP BY when editing → one row for the whole table (43,879 rows in one pile)

### Interview Q&A
- ⭐⭐⭐ **How does the query run?** FROM → WHERE (88 rows) → GROUP BY (one pile per district) → aggregates → SELECT → ORDER BY
- ⭐⭐⭐ **Limitations?** Some districts rest on 1 area; unweighted average of averages; "Dublin" county mixes different towns
- ⭐⭐ **Why show COUNT next to AVG?** Shows how much data each average rests on, so readers can judge reliability
- ⭐⭐ **AVG without GROUP BY?** The whole table becomes one group → one row
- ⭐⭐ **Weighted average?** Each value counts by its size; needs tenancy counts we don't have
- ⭐ **NameError / IndentationError?** Name not defined at that point / unexpected indent breaks Python's structure