from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "rent_annual_raw.csv"
CLEAN_FILE = PROJECT_ROOT / "data" / "rent_dublin_clean.csv"

# 0. Load raw data (as text, then convert rent to numbers)
df = pd.read_csv(RAW_FILE, dtype=str)
df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")
print("Raw rows:", len(df))

# 1. Keep useful columns and give them clean names
df = df[["Year", "Number of Bedrooms", "Property Type",
         "C03004V03625", "Location", "VALUE"]].rename(columns={
    "Year": "year",
    "Number of Bedrooms": "bedrooms",
    "Property Type": "property_type",
    "C03004V03625": "location_code",
    "Location": "location",
    "VALUE": "avg_rent",
})
df["year"] = df["year"].astype(int)

# 2. Split "Arbour Hill, Dublin 7" -> area = "Arbour Hill", district = "Dublin 7"
parts = df["location"].str.rsplit(",", n=1, expand=True)
df["area"] = parts[0].str.strip()
df["district"] = parts[1].str.strip().fillna(df["area"])

# 3. Keep only Dublin (the district part must start with "Dublin")
df = df[df["district"].str.startswith("Dublin")].copy()
print("Dublin rows:", len(df))

# 4. Drop rows where the RTB suppressed the rent
missing = df["avg_rent"].isna().sum()
df = df.dropna(subset=["avg_rent"])
print("Dropped (no rent):", missing, "| Rows kept:", len(df))

# 5. Checks before saving
print("Years:", df["year"].min(), "to", df["year"].max())
print("Areas:", df["area"].nunique(), "| Districts:", df["district"].nunique())
print(sorted(df["district"].unique()))
print(df.head())

# 6. Save
df.to_csv(CLEAN_FILE, index=False)
print("Saved to:", CLEAN_FILE)