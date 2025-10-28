import csv
import mysql.connector
import time

CSV_FILE = "Library_Usage.csv"

def parse_bool(value): # Helper function for booleans in the CSV
    v = value.strip().lower()
    if v == 'true':
        return 1
    elif v == 'false':
        return 0
    else:
        return None

# Connect to server
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )
    
    if connection.is_connected():
        print(f"successfully connected to the server\n")
        cursor = connection.cursor()
except Exception as e:
    print(f"error while connecting to the server: {e}")

start_time = time.time()    
cursor.execute("CREATE DATABASE IF NOT EXISTS sfils_db;")
cursor.execute("USE sfils_db;")
    
cursor.execute('''
CREATE TABLE IF NOT EXISTS PATRONTYPES (
    Patron_Type_Definition VARCHAR(50) PRIMARY KEY
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS AGERANGES (
    Age_Range VARCHAR(50) PRIMARY KEY
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS LIBRARIES (
    Home_Library_Definition VARCHAR(100) PRIMARY KEY
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS NOTICES (
    Notice_Preference_Definition VARCHAR(20) PRIMARY KEY
);
''')
    
cursor.execute('''
CREATE TABLE IF NOT EXISTS PATRONS (
    Patron_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patron_Type_Definition VARCHAR(50) NOT NULL,
    Total_Checkouts INT,
    Total_Renewals INT,
    Age_Range VARCHAR(50),
    Home_Library_Definition VARCHAR(100) NOT NULL,
    Circulation_Active_Month VARCHAR(20),
    Circulation_Active_Year VARCHAR(10),
    Notice_Preference_Definition VARCHAR(20),
    Provided_Email_Address BOOLEAN,
    Year_Patron_Registered VARCHAR(10),
    Within_San_Francisco_County BOOLEAN,
    FOREIGN KEY (Patron_Type_Definition) REFERENCES PATRONTYPES(Patron_Type_Definition),
    FOREIGN KEY (Age_Range) REFERENCES AGERANGES(Age_Range),
    FOREIGN KEY (Home_Library_Definition) REFERENCES LIBRARIES(Home_Library_Definition),
    FOREIGN KEY (Notice_Preference_Definition) REFERENCES NOTICES(Notice_Preference_Definition)
);
''')

patron_types = set()
age_ranges = set()
libraries = set()
notices = set()
rows = []

with open(CSV_FILE, encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    
    columns = [ # Hard coded column names due to 'Unknown column' error
        'Patron_Type_Definition',
        'Total_Checkouts',
        'Total_Renewals',
        'Age_Range',
        'Home_Library_Definition',
        'Circulation_Active_Month',
        'Circulation_Active_Year',
        'Notice_Preference_Definition',
        'Provided_Email_Address',
        'Year_Patron_Registered',
        'Within_San_Francisco_County'
    ]
    
    query = 'INSERT INTO PATRONS ({0}) VALUES ({1})'
    query = query.format(
        ','.join(f'`{c}`' for c in columns),
        ','.join(['%s'] * len(columns))
    )
    
    print(f"importing, please wait...\n")
    for data in reader:
        data[8] = parse_bool(data[8])
        data[10] = parse_bool(data[10])
        for i in [1,2]: # Int typechecking for Int columns
            try:
                data[i] = int(data[i]) if data[i].strip() else None
            except ValueError:
                data[i] = None # If we get something other than a number
        
        # Adds values to sets for other tables, sets are used to ensure no duplicates are added.
        patron_types.add(data[0])
        age_ranges.add(data[3])
        libraries.add(data[4])
        notices.add(data[7])
        rows.append(data)
    
# INSERT IGNORE used to ensure no duplicates are entered.
for p in patron_types:
    cursor.execute("INSERT IGNORE INTO PATRONTYPES (Patron_Type_Definition) VALUES (%s)", (p,))
for a in age_ranges:
    cursor.execute("INSERT IGNORE INTO AGERANGES (Age_Range) VALUES (%s)", (a,))
for l in libraries:
    cursor.execute("INSERT IGNORE INTO LIBRARIES (Home_Library_Definition) VALUES (%s)", (l,))
for n in notices:
    cursor.execute("INSERT IGNORE INTO NOTICES (Notice_Preference_Definition) VALUES (%s)", (n,))
connection.commit()
    
for data in rows:
    cursor.execute(query, data)
connection.commit()
end_time = time.time()
duration = end_time - start_time    
print(f"CSV successfully converted in {duration:.3f} seconds! exiting...\n")    
cursor.close()
connection.close()