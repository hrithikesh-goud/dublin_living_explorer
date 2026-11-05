import os
from datetime import datetime, timezone

import pandas as pd
import requests
from sqlalchemy import create_engine

STATUS_URL = "https://api.cyclocity.fr/contracts/dublin/gbfs/station_status.json"
INFO_URL = "https://api.cyclocity.fr/contracts/dublin/gbfs/station_information.json"

engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)


def lambda_handler(event, context):
    status = requests.get(STATUS_URL, timeout=30)
    status.raise_for_status()
    info = requests.get(INFO_URL, timeout=30)
    info.raise_for_status()

    status_df = pd.DataFrame(status.json()["data"]["stations"])
    info_df = pd.DataFrame(info.json()["data"]["stations"])

    bikes = status_df.merge(info_df, on="station_id", how="left")
    bikes = bikes[["station_id", "name", "num_bikes_available",
                   "num_docks_available", "capacity", "lat", "lon"]].copy()
    bikes["fetched_at"] = datetime.now(timezone.utc)

    bikes.to_sql("bike_snapshots", engine, if_exists="append", index=False)
    print(f"Saved {len(bikes)} rows to bike_snapshots")
    return {"rows_saved": len(bikes)}