# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:42:15 2024

MycoBank API

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

#url = "https://webservices.bio-aware.com/cbsdatabase_new/Mycobank%20WS"
#url = "https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames"
#url = "https://webservices.bio-aware.com/cbsdatabase_new/Mycobank%20WS?page=10&pageSize=100"
#url = "https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?page=1&pageSize=1200&filter=name startWith %27Abortiporus%27"
url = "https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?page=5&pageSize=1200&"

#for page in range(1,449):
#    url = 'https://webservices.bio-aware.com/cbsdatabase_new/mycobank/taxonnames?page=2&pageSize=1200&'%page
#    myResponse = requests.get(url, verify=True, headers=headers)


# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
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

df.to_excel('mycobank.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})