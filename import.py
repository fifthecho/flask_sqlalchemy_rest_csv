import csv
import requests
import json
from app import db
db.create_all()

with open('FL_insurance_sample.csv', 'r') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        to_import = {}
        to_import['policyID'] = row['policyID']
        to_import['statecode'] = row['statecode']
        to_import['county'] = row['county']
        to_import['eq_site_limit'] = row['eq_site_limit']
        to_import['hu_site_limit'] = row['hu_site_limit']
        results = requests.post('http://localhost:5000/policy', data = json.dumps(to_import))
        print(results.text)
