import requests

url = "https://api.aevo.xyz/markets"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

data = response.json()

filtered_data = [
    {
        "instrument_id": item["instrument_id"],
        "instrument_name": item["instrument_name"],
        "instrument_type": item["instrument_type"], 
        "underlying_asset": item["underlying_asset"]
    }
    for item in data
]

print(filtered_data)
