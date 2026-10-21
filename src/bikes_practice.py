import requests
URL = "https://api.cyclocity.fr/contracts/dublin/gbfs/station_status.json"
response = requests.get(URL, timeout=30)
print(response.status_code)
data = response.json()
print(data.keys())
stations = data["data"]["stations"]
print(len(stations))
print(stations[0])
print(stations[0]["num_bikes_available"])