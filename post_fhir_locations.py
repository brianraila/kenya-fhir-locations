#!/usr/bin/python3

## Author: Brian R. Amolo <railamolo@gmail.com>

import json, requests, csv
from sys import argv


FHIR_BASE = "{}/Location".format(argv[1])
    



with open("kenya_locations.csv", "r") as csvfile:
    csvreader = csv.DictReader(csvfile)
    sub_counties = []
    # Iterate over each row in the CSV file
    data = {
            "resourceType":"Location",
            "id": 0,
            "name":"Kenya",
            "active":"true",
        }
    response = requests.put("{}/{}".format(FHIR_BASE, 0), json=data).json()
    print(response)
    for row in csvreader:
        if row['SubCounty'] == '': # is county
            data = {
                "resourceType":"Location",
                "id": row['id'],
                "name":row['County'],
                "active":"true",
                "partOf":{"reference":"Location/0"}
            }
            response = requests.put("{}/{}".format(FHIR_BASE, row['id']), json=data).json()
            print(response)
        elif row['SubCounty'] != '':
            sub_county = {"name":row['SubCounty'], "county":row['County']}
            
            if not row['SubCounty'] in sub_counties:
                data = {
                "resourceType":"Location",
                "id":(row["SubCounty"]).upper(). replace(" ", "-").replace("'", ""),
                "name":(row["SubCounty"]).upper(),
                "active":"true",
                "partOf":{"reference":"Location/{}".format((row['County']).upper(). replace(" ", "-").replace("'", ""))}
                }
                response = requests.put("{}/{}".format(FHIR_BASE, sub_county['name'].upper(). replace(" ", "-").replace("'", "")), json=data).json()
                print(response)
                sub_counties.append(row['SubCounty'])
            ward = {"name":row['Ward'], "sub_county":row['SubCounty'] }
            data = {
                "resourceType":"Location",
                "id": ward['name'].upper().replace(" ", "-").replace("'", ""),
                "name": (ward['name']).upper(),
                "active":"true",
                "partOf":{"reference":"Location/{}".format(row['SubCounty'].upper(). replace(" ", "-").replace("'", ""))}
            }
            response = requests.put("{}/{}".format(FHIR_BASE, ward['name'].upper(). replace(" ", "-").replace("'", "")), json=data).json()
            print(response)




       



