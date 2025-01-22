# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:45:26 2025

@author: mcveigh
"""

import pandas as pd
import requests
import re
import json
from pandas import json_normalize
import os
import sys
#import subprocess
import xlsxwriter

import requests
from requests.auth import HTTPDigestAuth
import json
result = []

headers = {"Content-Type": "application/json; charset=utf-8; Accept"}

def get_all_data(base_url):
    """Fetches all data from a paginated API."""

    page_number = 1
    all_data = []

    while True:
        url = f"{base_url}?page={page_number}" 
        response = requests.get(url)

        if response.status_code != 200:
            break

        data = response.json()

        # Check if there's more data
        if not data:
            break

        all_data.extend(data)
        page_number += 1
        print("page number is", page_number)
    return all_data

base_url = "https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?pageSize=1200&"
all_data = get_all_data(base_url)

for i in all_data['items']:
    #print("Name:", ['contact.webUrl'])
    result.append(i)
    df = json_normalize(result)
print(df)

df.to_excel('mycobank_all.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})