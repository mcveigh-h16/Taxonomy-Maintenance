# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 08:15:17 2024

REST API to extract institution data from Index Herbarium by date search
https://sweetgum.nybg.org/science/ih/

@author: mcveigh
"""

import pandas as pd
import numpy as np
import requests
import re
import json
from pandas import json_normalize
import os
import sys
import subprocess
import xlsxwriter

import requests
from requests.auth import HTTPDigestAuth
import json

url = "http://sweetgum.nybg.org/science/api/v1/institutions/search?dateModified=>1/1/2023"
result = []

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
myResponse = requests.get(url, verify=True)


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
    for i in jData['data']:
        #print("Name:", ['contact.webUrl'])
        result.append(i)
    df = json_normalize(result)
    df.replace('[]', pd.NA)
    new_df = df.drop(columns=['specimenTotal', 'geography', 'incorporatedHerbaria', 'importantCollectors',  'notes', 'address.postalCountry',
                              'contact.phone', 'location.lat', 'location.lon', 'collectionsSummary.numAlgae', 'collectionsSummary.numAlgaeDatabased',
                              'collectionsSummary.numAlgaeImaged', 'collectionsSummary.numBryos', 'collectionsSummary.numBryosDatabased',
                              'collectionsSummary.numBryosImaged', 'collectionsSummary.numFungi', 'collectionsSummary.numFungiDatabased',
                              'collectionsSummary.numFungiImaged', 'collectionsSummary.numPteridos', 'collectionsSummary.numPteridosDatabased',
                              'collectionsSummary.numPteridosImaged', 'collectionsSummary.numSeedPl', 'collectionsSummary.numSeedPlDatabased',
                              'collectionsSummary.numSeedPlImaged'])
    #print(new_df.head)
    
    
    new_df.to_excel('IndexHebarium.xlsx', engine='xlsxwriter', index = False, na_rep = '')  
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
    
#Get NCBI collections data from FTP site. Saves as a file in the working directory
import wget
link = 'https://ftp.ncbi.nih.gov/pub/taxonomy/Ccode_dump.txt'
wget.download(link)

ncbi_collections_df = pd.read_csv("Ccode_dump.txt", sep='|', index_col=None, low_memory=False, header=None, names=["coll_id", "inst_id", 
                                "coll_name", "coll_code", "coll_size", "collection_type", "coll_url_rule", "coll_url", "qualifier_type",
                                "comments"])
print(ncbi_collections_df.head)