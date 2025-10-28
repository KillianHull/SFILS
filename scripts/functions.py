import mysql.connector
import time

allowed_fields = [
        'Patron_ID', 'Patron_Type_Definition', 'Total_Checkouts', 'Total_Renewals', 
        'Age_Range', 'Home_Library_Definition', 'Circulation_Active_Month', 
        'Circulation_Active_Year', 'Notice_Preference_Definition', 
        'Provided_Email_Address', 'Year_Patron_Registered', 
        'Within_San_Francisco_County'
    ]

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="sfils_db"
    )
    
def get_all_patrons():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    start_time = time.time()
    cursor.execute("SELECT * FROM PATRONS")
    results = cursor.fetchall()
    end_time = time.time()
    print(f"\n{len(results)} patrons found.\n")
    duration = end_time - start_time
    print(f"Query finished in {duration:.3f} seconds\n")
    cursor.close()
    connection.close()
    clean_print(results)

def insert_patron(data):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = '''
        INSERT INTO PATRONS (
            Patron_Type_Definition, Total_Checkouts, Total_Renewals,
            Age_Range, Home_Library_Definition, Circulation_Active_Month,
            Circulation_Active_Year, Notice_Preference_Definition,
            Provided_Email_Address, Year_Patron_Registered,
            Within_San_Francisco_County
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    try:
        start_time = time.time()
        cursor.execute(query, data)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Query finished in {duration:.3f} seconds\n")
    except Exception as e:
        print(f"An error occured while inserting the patron: {e}")
        
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM PATRONS WHERE Patron_ID = %s", (new_id,))
    new_patron = cursor.fetchone()
    clean_print([new_patron])
        
    connection.commit()
    cursor.close()
    connection.close()
    
def update_patron(patron_id, field, new_val):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    if field not in allowed_fields:
        print(f"Error: {field} is not a valid field.")
        return
        
    if field in ['Provided_Email_Address', 'Within_San_Francisco_County']:
        if isinstance(new_val, str):
            v = new_val.strip().lower()
            if v == 'true':
                new_val = 1
            elif v == 'false':
                new_val = 0
            else:
                new_val = None
                
    if field in ['Total_Checkouts', 'Total_Renewals']:
        try:
            new_val = int(new_val)
        except ValueError:
            print("Invalid integer, update failed.")
            cursor.close()
            connection.close()
            return
    
    query = f"UPDATE PATRONS SET {field} = %s WHERE Patron_ID = %s"
    start_time = time.time()
    cursor.execute(query, (new_val, patron_id))
    connection.commit()
    end_time = time.time()
    print(f"Patron {patron_id} updated: {field} = {new_val}\n")
    duration = end_time - start_time
    print(f"Query finished in {duration:.3f} seconds\n")
    
    cursor.close()
    connection.close()
    
def clean_print(rows):
    counter = 0
    for r in rows:
        print("".join(f"{k}: {v}\n" for k, v in r.items()))
        print("\n")
        counter += 1
        if counter == 10:
            cont = input("Continue printing records? (yes/no): ")
            if cont.lower() == "yes":
                counter = 0
            else:
                break
                
def prompt_new_patron():
    data = []
    for field in allowed_fields:
        if field != "Patron_ID":
            while True:
                value = input(f"Enter {field} (leave blank for NULL): ").strip()
                
                if field in ['Total_Checkouts', 'Total_Renewals']:
                    if value == "":
                        data.append(None)
                        break
                    try:
                        data.append(int(value))
                        break
                    except ValueError:
                        print("Please enter a valid integer.")
                        
                elif field in ['Provided_Email_Address', 'Within_San_Francisco_County']:
                    if value.lower() in ['true', 't', '1']:
                        data.append(1)
                        break
                    elif value.lower() in ['false', 'f', '0']:
                        data.append(0)
                        break
                    elif value == "":
                        data.append(None)
                        break
                    else:
                        print("Please enter True or False.")
                        
                else:
                    data.append(value if value != "" else None)
                    break
    
    print("\n")
    return data
    
def search():
    field = input("Enter the field to search by: ")
    if field not in allowed_fields:
        print(f"Error: {field} is not a valid field.")
        return
    
    if field in ['Total_Checkouts', 'Total_Renewals']:
        try:
            val = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid integer, exiting search.")
    elif field in ['Provided_Email_Address', 'Within_San_Francisco_County']:
        val = input("Enter True or False (leave blank for NULL): ")
        if val.lower() in ['true', 't', '1']:
            val = 1
        elif val.lower() in ['false', 'f', '0']:
            val = 0
        else:
            val = None
    else:
        val = input("Enter the value: ")
        
    search_type = input("Enter 'exact' for exact matches, and 'like' for like matches. ")    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    start_time = time.time()
    
    if val is None:
        query = f"SELECT * FROM PATRONS WHERE {field} IS NULL"
        cursor.execute(query)
    else:
        if search_type.lower().strip() == "like":
            val = f"%{val}%" # This is needed so the % is still present in the query, and properly uses LIKE
            query = f"SELECT * FROM PATRONS WHERE {field} LIKE %s" # LIKE used to match all instances, not exact matches
        else: # Default to exact searches if search_type isn't like
            query = f"SELECT * FROM PATRONS WHERE {field} = %s" 
        cursor.execute(query, (val,))
        
    results = cursor.fetchall()
    end_time = time.time()
    print(f"\n{len(results)} patrons found.\n")
    duration = end_time - start_time
    print(f"Query finished in {duration:.3f} seconds\n")
    
    cursor.close()
    connection.close()
    
    print("\n")
    if results:
        clean_print(results)
    else:
        print("No results found.")
        
def delete_patron():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    patron_id = int(input("Enter the patron's ID you wish to delete: "))
    
    start_time = time.time()
    cursor.execute("SELECT * FROM PATRONS WHERE Patron_ID = %s", (patron_id,))
    result = cursor.fetchone()
    if not result:
        print(f"No patron with ID {patron_id} found.\n")
        cursor.close()
        connection.close()
        return
    
    cursor.execute("DELETE FROM PATRONS WHERE Patron_ID = %s", (patron_id,))
    connection.commit()
    print(f"Patron {patron_id} successfully deleted!\n")
    end_time = time.time()
    duration = end_time - start_time
    print(f"Query finished in {duration:.3f} seconds\n")
    
    cursor.close()
    connection.close()
    