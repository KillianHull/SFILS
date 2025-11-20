import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["sfils_db"]
collection = db["patrons"]

csv_path = "Library_Usage.csv"

with open(csv_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    data = []
    for row in reader:
        if row['Total Checkouts']:
            row['Total Checkouts'] = int(row['Total Checkouts'].replace(',', ''))
        else:
            row['Total Checkouts'] = None
            
        if row['Total Renewals']:
            row['Total Renewals'] = int(row['Total Renewals'].replace(',', ''))
        else:
            row['Total Renewals'] = None
            
        for response in ['Provided Email Address', 'Within San Francisco County']:
            if row[response].lower() == "true":
                row[response] = True
            elif row[response].lower() == "false":
                row[response] = False
            else:
                row[response] = None
                
        not_null = ["Patron Type", "Total Checkouts", "Total Renewals", "Age Range", "Home Library Definition"]
        for response in row:
            if response not in not_null:
                val = row[response]
                if isinstance(val, str) and val.lower() == "null":
                    row[response] = None
        data.append(row)
        
if data:
    collection.insert_many(data)
    print(f"{len(data)} documents inserted into patrons.")
else:
    print("no data found in csv.")