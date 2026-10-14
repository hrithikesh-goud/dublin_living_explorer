from pathlib import Path
import io
 
import pandas as pd
import requests
 
# 1. Where to save: the project's data folder (works no matter where you run it from)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
 
# 2. Where to get it: CSO PxStat API, table RIA02 (RTB average monthly rent, annual)
URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/RIA02/CSV/1.0/en"
 
# 3. Download (browser-like headers so the CSO server accepts the request)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "text/csv,application/json;q=0.9,*/*;q=0.8",
}
response = requests.get(URL, headers=headers, timeout=60)
print("Status code:", response.status_code)

response.raise_for_status()
text = response.content.decode("utf-8-sig")        # utf-8-sig removes the BOM
df = pd.read_csv(io.StringIO(text), dtype=str)     # read all as text: no mixed-type guessing
df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")  # rent becomes a number
 
# 4. Save a raw copy
out_file = DATA_DIR / "rent_annual_raw.csv"
df.to_csv(out_file, index=False)
 
# 5. First look at the data
print("Saved to:", out_file)
print("Rows, columns:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())