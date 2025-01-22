# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:58:57 2025

API for extracting data from Mycobank per communication with Vincient Robert at mycobank. 
The limit is 1200 rows of data per page. Determined there are 449 pages currently available.
Script steps through page by page 1-449 (max_number) to extract data and append it to a 
dataframe. 

@author: mcveigh
"""

# -*- coding: utf-8 -*-


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

#works to extract data one page at a time. Determined there are currently 449 pages of information available.
#url = "https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?page=1&pageSize=1200&"



start_number = 1
max_number = 449
    
for number in range(start_number, max_number + start_number):
    print(number)
    url = ('https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?page=' + str(number) +'&pageSize=1200&')
    myResponse = requests.get(url, verify=True, headers=headers)



    print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
    if(myResponse.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)


        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        #print(jData)
        for i in jData['items']:
            #print("Name:", ['contact.webUrl'])
            result.append(i)
df = json_normalize(result)
print(df)

df.to_excel('mycobank449.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})