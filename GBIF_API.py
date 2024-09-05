# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 13:05:11 2024

REST API to extract institution data from GRSciColl
https://techdocs.gbif.org/en/openapi/v1/registry

https://pygbif.readthedocs.io/en/latest/

https://github.com/gbif/pygbif

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
from requests.auth import HTTPDigestAuth

from pygbif import registry
url = "https://api.gbif.org/v1/dataset"
myResponse = requests.get(url, verify=True)

print (myResponse.status_code)
data =[]

#test = registry.dataset_search(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')

if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)
    print("The response contains {0} properties".format(len(jData)))
    #print(jData)
    for result in jData['results']:
        #print("Name:", ['contact.webUrl'])
        data.append(result)
    df = json_normalize(data)
    print(df)
    
    
    #result = registry.installations(q="france")
    #jData = json.loads(myResponse.content)
    #for i in jData:
        #print("Name:", ['contact.webUrl'])
        #result.append(i)
    #df = json_normalize(result)
    

else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()


#df.to_excel('GBIF.xlsx', engine='xlsxwriter', index = False, na_rep = '')
#print(test)