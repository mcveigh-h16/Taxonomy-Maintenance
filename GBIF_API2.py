# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 08:25:38 2024

REST API to extract institution data from GRSciColl
https://techdocs.gbif.org/en/openapi/v1/registry

https://pygbif.readthedocs.io/en/latest/

https://github.com/gbif/pygbif

@author: mcveigh
"""

import pandas as pd
import numpy as np
import requests
import re
import json
from pandas import json_normalize
#import os
#import sys
#import subprocess
import xlsxwriter
from requests.auth import HTTPDigestAuth


data = []
step= 200
offset = 0
endOfRecords = False

while not endOfRecords:
    institution_request = requests.get('https://api.gbif.org/v1/grscicoll/institution?identifierType=NCBI_BIOCOLLECTION'+'&limit='+str(step)+'&offset='+str(offset))
    offset += step
    if institution_request.ok:
        institutions_res = institution_request.json()
        endOfRecords = institutions_res["endOfRecords"]
        data.append(institutions_res)

    else:
        endOfRecords = True
df = json_normalize(data, record_path='results')
df["types"] = df["types"].str.replace('[]','')

print(df.iloc[0,0:8])
df.to_excel('GBIF.xlsx', engine='xlsxwriter', index = False, na_rep = '')

#Get NCBI collections data from FTP site. Saves as a file in the working directory
#Can turn this off if already populated
import wget
link = 'https://ftp.ncbi.nih.gov/pub/taxonomy/biocollections/Collection_codes.txt'
wget.download(link)

fin = open("Collection_codes.txt", "r") 
fout = open("Collection_codes2.txt", "w")
for line in fin:
   new_line = line.replace('\t', '')
   fout.write(new_line) 
fin.close()
fout.close()

ncbi_collection_codes = pd.read_csv("Collection_codes.txt", sep='|', low_memory=False, header=0)
print(ncbi_collection_codes.head)
ncbi_collection_codes.to_excel('ncbi_collection_codes.xlsx', engine='xlsxwriter', index = False, na_rep = '')
