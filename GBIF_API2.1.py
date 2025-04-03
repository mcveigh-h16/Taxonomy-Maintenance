# -*- coding: utf-8 -*-
"""

REST API to extract institution data from GRSciColl
https://techdocs.gbif.org/en/openapi/v1/registry

https://pygbif.readthedocs.io/en/latest/

https://github.com/gbif/pygbif

Created on Thu Oct  3 08:10:49 2024

@author: mcveigh
"""

import pandas as pd
import numpy as np
import requests
import re
import json
from pandas import json_normalize
#import os
import sys
#import subprocess
import xlsxwriter
from requests.auth import HTTPDigestAuth


data = []
step= 200
offset = 0
endOfRecords = False
status = True

while not endOfRecords:
    # for gbif data with NCBI identifiers
    #institution_request = requests.get('https://api.gbif.org/v1/grscicoll/institution?identifierType=NCBI_BIOCOLLECTION'+'&limit='+str(step)+'&offset='+str(offset))
    # for all gbif data
    institution_request = requests.get('https://api.gbif.org/v1/grscicoll/institution?'+'&limit='+str(step)+'&offset='+str(offset))
    offset += step
    if institution_request.ok:
        institutions_res = institution_request.json()
        endOfRecords = institutions_res["endOfRecords"]
        data.append(institutions_res)

    else:
        endOfRecords = True
df = json_normalize(data, record_path='results')
print(df)

#df.to_excel('GBIF_ALL.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})

gbifdf = df.drop(columns=['types', 'phone', 'institutionalGovernances', 'disciplines', 'latitude', 'longitude', 'additionalNames', 
                          'createdBy', 'modifiedBy', 'created', 'modified', 'tags', 'identifiers', 'contactPersons', 'machineTags',
                          'alternativeCodes', 'comments', 'occurrenceMappings', 'occurrenceCount', 'typeSpecimenCount', 'mailingAddress.key',
                          'address.key', 'mailingAddress.city', 'mailingAddress.province', 'mailingAddress.postalCode'])

gbifdf.to_excel('GBIF_all_drops.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})

#Get NCBI collections data from FTP site. Saves as a file in the working directory
#Can turn this off if already populated
#import wget
#link = 'https://ftp.ncbi.nih.gov/pub/taxonomy/biocollections/Collection_codes.txt'
#wget.download(link)

fin = open("Collection_codes.txt", "r") 
fout = open("Collection_codes2.txt", "w")
for line in fin:
   new_line = line.replace('\t', '')
   fout.write(new_line) 
fin.close()
fout.close()

print(gbifdf.dtypes)
ncbi_collection_codes = pd.read_csv("Collection_codes2.txt", sep='|', low_memory=False, header=0)
#ncbi_collection_codes['coll_code'] = ncbi_collection_codes['coll_code'].astype(object)
print(ncbi_collection_codes.dtypes)
ncbi_collection_codes.to_excel('ncbi_collection_codes.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})

combine_df=pd.merge(left=gbifdf, right=ncbi_collection_codes, left_on='code', right_on='coll_name', how = 'outer')
print(combine_df.head)
combine_df.to_excel('GBIF_REG_ALL_NCBI_combined.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})

if status:
    print("Script executed successfully! Output saved as GBIF_REG_ALL_NCBI_combined.xlsx")
    sys.exit(0) # Exit with success code
else:
    print("Script failed.")
    sys.exit(1) # Exit with an error code