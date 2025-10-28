import mysql.connector
from scripts import functions

while True:
    print("1. View all patrons")
    print("2. Add new patron")
    print("3. Update patron info")
    print("4. Search for a patron")
    print("5. Delete a patron")
    print("6. Exit")
    choice = input("Select an option: ")
    
    if choice == "1":
        functions.get_all_patrons() 
    elif choice == "2":
        data = functions.prompt_new_patron()
        functions.insert_patron(data)
    elif choice == "3":
        patron_id = int(input("Enter Patron ID to update: "))
        field = input("Enter field to update: ")
        new_value = input("Enter new value: ")
        functions.update_patron(patron_id, field, new_value)
    elif choice == "4":
        functions.search()
    elif choice == "5":
        functions.delete_patron()
    elif choice == "6":
        break
    else:
        print("Invalid choice.")