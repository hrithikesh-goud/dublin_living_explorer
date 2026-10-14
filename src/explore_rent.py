from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT_ROOT / "data" / "rent_annual_raw.csv", dtype=str)
df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")

print("1. YEARS:", df["Year"].min(), "to", df["Year"].max())

print("\n2. BEDROOM OPTIONS:")
print(df["Number of Bedrooms"].value_counts())

print("\n3. PROPERTY TYPES:")
print(df["Property Type"].value_counts())

print("\n4. MISSING RENTS:", df["VALUE"].isna().sum(), "of", len(df),
      f"({df['VALUE'].isna().mean():.0%})")

dublin = df[df["Location"].str.contains("Dublin", case=False, na=False)]
print("\n5. DUBLIN LOCATIONS:", dublin["Location"].nunique())
print(sorted(dublin["Location"].unique()))