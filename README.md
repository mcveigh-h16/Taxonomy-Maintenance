# Taxonomy-Maintenance

**lpsn_rest_api.py**
LSPN REST API to download their latest release and compare it to NCBI taxonomy. Currently the search date is hard coded into script

https://confluence.ncbi.nlm.nih.gov/display/TAX/Integrating+LPSN%2C+Index+Herbariorum%2C+and+GRSciColl+APIs+for+Taxonomy+Database+Maintenance+and+Curation

https://api.lpsn.dsmz.de/client_examples https://pypi.org/project/lpsn/

**GBIF_API2.1.py**

PC based. Downloads registery information from GBIF. https://techdocs.gbif.org/en/openapi/v1/registry compares it to NCBI data. Optional lines to toggle between all GBIF data and GBIF data with NCBI identifers. 

**GBIF_species_API.py** 

PC based. Downloads species information from GBIF. Working but decided not to pursue further at this time. 

**mycobankAPI.py**

PC based. Works to download data from mycobank in a page wise manner but mycobankAPIstepwise.py works to capture all data by page. Outputs to an excel file. mycobankAPIstewise.py will capture all data and is preferred, see below.

**mycobankAPIstewise.py**

PC based. API for extracting data from Mycobank per communication with Vincient Robert at mycobank. 
The limit is 1200 rows of data per page. Determined there are 449 pages currently available.
Script steps through page by page 1-449 (max_number) to extract data and append it to a 
dataframe. Outputs to an excel file. 

**Mycobankparser.ipynb**

PC based jupyter notebook. Combines and parses data from the API download and the excel file download from Mycobank's web site. Outputs to excel or csv file. NOTE output file will be very large and contain URLs, excel has hard limits on file size and number of URLs in the file which can result in a truncated file. Can you avoid this by outputting as csv file but testing confirmed this resulted in some non-ascii characters being modified. This functionality was added into PDFminer2.ipynb to avoid this file size limitation. See https://github.com/mcveigh-h16/PDF-Miner

**index_hebarium_api.py**

REST API to extract institution data from Index Herbarium by date search. Runs on PC and doesn't require linux.
https://sweetgum.nybg.org/science/ih/

https://github.com/nybgvh/IH-API/wiki

NCBI collection data from FTP site. This one is the most up to date one since Entrez Biocollections is no longer supported. Institution codes:

https://ftp.ncbi.nih.gov/pub/taxonomy/Ccode_dump.txt

Download NCBI collection data and compare to Index Herbarium by collection code. 
IH changed the format of the response. I changed for i in jData['key']: to for i in jData['results']:

dependencies
pandas
xlsxwriter

 
