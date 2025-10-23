#!/usr/bin/env python
# coding: utf-8

import requests
url = 'http://127.0.0.1:9696/predict'

result = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

response = requests.post(url,json=result).json()
print(response['c_probability'])
