# Scripts

csv_conversion.py is the script used to convert the CSV file into the database. This script assumes that the CSV file is named identically and located in the same directory as the script. Line 4 can be updated to the CSV's name and directory on your computer for it to work properly.

functions.py contains all of the functionality used by the frontend app to interface with and query the database. It contains basic implementation of all CRUD operations.

mongodb_conversion.py is the script used to convert the CSV file into the MongoDB database. This script assumes that the CSV file is named identically and located in the same directory as the script. Line 8 can be updated to the CSV's name and directory for it to work properly. Additionally, it may be necesary to modify line 4 to correctly connect to your local MongoDB instance.