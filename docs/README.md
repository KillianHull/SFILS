# Project Documentation

To properly create the database and run the python app, make sure the MySQL server is already running on your PC, then follow the steps below:

1. From command prompt, navigate into the scripts folder with the command 'cd path-to-SFILS\scripts'.

2. Make sure that the CSV file is named 'Library_Usage.csv' and that the file is also located in the scripts folder. Line 5 of csv_conversion.py can be updated to use the proper name and/or path of your CSV if it's in a different location.

3. Additionally, if your MySQL instance is configured with a different username and password than mine, it's necessary to update that in lines 20 and 21.

4. When csv_conversion.py is properly set up, run it in command prompt using the command 'python csv_conversion.py'

5. You'll get a message in the terminal once the conversion is complete. Once it is, cd out into the main SFILS directory using the command 'cd ..'

6. Once in the main SFILS directory, you're ready to run the app. Use the command 'python -m app.app' to run the program in command prompt.

# **app.py**
app.py showcases five main functions:
The first returns all library patrons in ascending order of Patron_ID. 
The second uses INSERT INTO queries to add new patrons to the database. 
The third uses UPDATE queries to update a given field about a patron. 
The fourth uses SELECT queries to search through the database with given paramaters. 
The fifth uses DELETE queries to remove patrons from the database. 

# MongoDB Project Documentation

To properly create the database and run the python app, make sure the MongoDB server is already running on your PC, then follow the steps below:

1. From command prompt, navigate into the scripts folder with the command 'cd path-to-SFILS\scripts'.

2. Make sure that the CSV file is named 'Library_Usage.csv' and that the file is also located in the scripts folder. Line 8 of mongodb_conversion.py can be updated to use the proper name and/or path of your CSV if it's in a different location.

3. Additionally, if your MongoDB instance is configured with a path, it's necessary to update that on line 4.

4. When mongodb_conversion.py is properly set up, run it in command prompt using the command 'python mongodb_conversion.py'

5. You'll get a message in the terminal once the conversion is complete. Once it is, cd out into the main SFILS directory using the command 'cd ..', and then into the mongo folder with 'cd mongo'

6. If your path on step 3 was different than mine, it's necessary to update this line in MongoApp.py on line 4 as well.

7. Once in the mongo directory, and it's properly configured, you're ready to run the app. Use the command 'python MongoApp.py' to run the program in command prompt.

# **MongoApp.py**
MongoApp.py showcases the same five functions as the original MySQL app:
The first returns all library patrons. 
The second adds new patrons to the database. 
The third updates a given field about a patron. 
The fourth searches through the database with given paramaters, working with both exact and like matches. 
The fifth removes patrons from the database. 

# Misc.
I'm unsure of where else to specify this, but I feel as if it's important information as it caused me hours of headaches: DO NOT PIP INSTALL BSON, AS IT WILL BREAK PYMONGO AND REQUIRE A FULL REINSTALL. PYMONGO ALREADY INCLUDES THE BSON LIBRARY IN ITS OWN INSTALL, AND INSTALLING THE BSON PACKAGE ON IT'S OWN MAKES PYMONGO DYSFUNCTIONAL.