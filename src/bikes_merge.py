import pandas as pd
import requests
from datetime import datetime, timezone
from pathlib import Path
BIKES_URL = "https://api.cyclocity.fr/contracts/dublin/gbfs/station_status.json"
INFO_URL =  "https://api.cyclocity.fr/contracts/dublin/gbfs/station_information.json"

#Fetching the bike data
BIKES_RESPONSE = requests.get(BIKES_URL, timeout = 30)
print("Status Code:",BIKES_RESPONSE.status_code)
status_bikes = BIKES_RESPONSE.json()["data"]["stations"]

#Fetching the information and area
INFO_RESPONSE = requests.get(INFO_URL, timeout = 30)
print("Status code:",INFO_RESPONSE.status_code)
Info_Address = INFO_RESPONSE.json()["data"]["stations"]

status_df = pd.DataFrame(status_bikes)
info_df = pd.DataFrame(Info_Address)
print(status_df)
print(info_df)
print("STATUS Columns",status_df.columns.tolist())
print("INFO Columns",info_df.columns.tolist())
left_result = status_df.merge(info_df, on ="station_id" ,how ="left")
print("LEFT JOIN:")
print(left_result)
inner_result = status_df.merge(info_df, on ="station_id", how = "inner")
print("INNER JOIN:")
print(inner_result)
print("Left rows:",len(left_result))
print("Inner rows:",len(inner_result))
print("Stations with no name:",left_result["name"].isna().sum())
bikes = left_result[["station_id","name","num_bikes_available","num_docks_available",
                  "capacity", "lat", "lon"]]
print(bikes.head())
print(bikes.shape)
# Add the time this snapshot was taken (UTC)
bikes = bikes.copy()
bikes["fetched_at"] = datetime.now(timezone.utc)

# Save: add to the bottom of the file, header only the first time
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = PROJECT_ROOT / "data" / "bikes_snapshots.csv"

bikes.to_csv(SNAPSHOT_FILE, mode="a", header=not SNAPSHOT_FILE.exists(), index=False)
print("Saved", len(bikes), "rows to", SNAPSHOT_FILE)