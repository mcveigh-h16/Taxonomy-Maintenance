# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 12:22:47 2024

https://www.indexfungorum.org/ixfwebservice/fungus.asmx?op=NameSearch

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
    institution_request = requests.get('https://.indexfungorum.org/ixfwebservice/fungus.asmx/NameSearch?Gloeopeniophorella=string&AnywhereInText=string&MaxNumber=string?')
    offset += step
    if institution_request.ok:
        institutions_res = institution_request.json()
        endOfRecords = institutions_res["endOfRecords"]
        data.append(institutions_res)

    else:
        endOfRecords = True
df = json_normalize(data, record_path='results')
print(df)

