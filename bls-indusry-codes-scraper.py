import requests
import re
import csv

#get file with all bls industry codes
r = requests.get('https://download.bls.gov/pub/time.series/ce/ce.industry')

#each line is seperated by carriage return
lines = re.split('\r\n', r.text)

#each line is tab deliminated
headers = lines[0].split('\t')

rows = [ line.split('\t') for line in lines[1:]]

with open('industry-codes.csv', 'wt') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    
