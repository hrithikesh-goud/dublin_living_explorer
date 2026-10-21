import pandas as pd

status = [
    {"station_id": "1", "bikes": 3},
    {"station_id": "2", "bikes": 0},
    {"station_id": "5", "bikes": 7},
]

info = [
    {"station_id": "1", "name": "CLARENDON ROW"},
    {"station_id": "2", "name": "BLESSINGTON STREET"},
    {"station_id": "3", "name": "BOLTON STREET"},
]
status_df = pd.DataFrame(status)
info_df = pd.DataFrame(info)
print(info_df)
print(status_df)
left_result = status_df.merge(info_df, on="station_id", how="left")
print("LEFT JOIN:")
print(left_result)
inner_result = status_df.merge(info_df, on="station_id", how = "left")
print("INNER JOIN:")
print(inner_result)