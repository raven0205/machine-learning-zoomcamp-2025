#!/usr/bin/env python
# coding: utf-8

import requests
url = 'http://127.0.0.1:9696/predict'

data = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

raw_response = requests.post(url, json=data)

predictions = raw_response.json()

print(f"Conversion Probability: {predictions['c_probability']}") 
print(f"Converted: {predictions['converted']}")