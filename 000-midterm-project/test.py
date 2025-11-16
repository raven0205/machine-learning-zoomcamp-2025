# 000-midterm-project/test.py

import requests
url = "http://localhost:9696/predict" # ensure the same [port] as the app in predict.py

client = {
    "month": "2024-01",
    "town": "ANG MO KIO",
    "flat_type": "3 ROOM",
    "block": "308B",
    "street_name": "ANG MO KIO AVE 1",
    "storey_range": "01 TO 03",
    "floor_area_sqm": 70,
    "lease_commence_date": 2012
}
response = requests.post(url, json=client).json()
print(response)
