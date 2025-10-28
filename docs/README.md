# Project Documentation

To properly create the database and run the python app, make sure the MySQL server is already running on your PC, then follow the steps below:

1. From command prompt, navigate into the scripts folder with the command 'cd <path-to-SFILS>\scripts'.

2. Make sure that the CSV file is named 'Library_Usage.csv' and that the file is also located in the scripts folder. Line 4 of csv_conversion.py can be updated to use the proper name and/or path of your CSV if it's in a different location.

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