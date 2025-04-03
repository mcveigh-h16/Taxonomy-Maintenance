# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:39:55 2024

REST API to extract species data from GRSciColl
https://techdocs.gbif.org/en/openapi/v1/registry

https://pygbif.readthedocs.io/en/latest/

https://github.com/gbif/pygbif


@author: mcveigh
"""

# -*- coding: utf-8 -*-

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
status = True

data = []
step= 200
offset = 0
endOfRecords = False

while not endOfRecords:
    # for gbif data with NCBI identifiers
    #institution_request = requests.get('https://api.gbif.org/v1/grscicoll/institution?identifierType=NCBI_BIOCOLLECTION'+'&limit='+str(step)+'&offset='+str(offset))
    # for all gbif data
    institution_request = requests.get('https://api.gbif.org/v1/species?'+'&limit='+str(step)+'&offset='+str(offset))
    offset += step
    if institution_request.ok:
        institutions_res = institution_request.json()
        endOfRecords = institutions_res["endOfRecords"]
        data.append(institutions_res)

    else:
        endOfRecords = True
df = json_normalize(data, record_path='results')
print(df)

df.to_excel('GBIF_species.xlsx', engine='xlsxwriter', index = False, na_rep = '', engine_kwargs={'options': {'strings_to_urls': False}})

if status:
    print("Script executed successfully! Output saved as GBIF_species.xlsx")
    sys.exit(0) # Exit with success code
else:
    print("Script failed.")
    sys.exit(1) # Exit with an error code