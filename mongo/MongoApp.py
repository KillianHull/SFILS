import pymongo
from bson import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sfils_db"]
collection = db["patrons"]

def clean_print(docs):
    counter = 0
    for doc in docs:
        for k, v in doc.items():
            print(f"{k}: {v}")
        print("\n")
        counter += 1
        if counter == 10:
            cont = input("Continue printing records? (y/n): ")
            if cont.lower() == "y":
                counter = 0
            else:
                break

def return_all():
    records = list(collection.find())
    clean_print(records)

def add_patron():
    patron = {}
    fields = [
        'Patron Type Definition', 'Total Checkouts', 'Total Renewals', 'Age Range',
        'Home Library Definition', 'Circulation Active Month', 'Circulation Active Year',
        'Notice Preference Definition', 'Provided Email Address', 'Year Patron Registered', 'Within San Francisco County'
    ]
    
    for field in fields:
        value = input(f"Enter {field} (leave blank for null): ").strip()
        if value == "":
            patron[field] = None
        elif field in ['Total Checkouts', 'Total Renewals']:
            patron[field] = int(value)
        elif field in ['Provided Email Address', 'Within San Francisco County']:
            if value.lower() in ['true','t']:
                patron[field] = True
            elif value.lower() in ['false','f']:
                patron[field] = False
            else:
                patron[field] = None
        else:
            patron[field] = value
            
    new_patron = collection.insert_one(patron)
    print(f"\nNew patron inserted with id: {new_patron.inserted_id}")
    
def update_patron():
    patron_id = input("Enter the id of the patron to update: ").strip()
    field = input("Enter the field to update: ").strip()
    new_value = input("Enter the new value: ").strip()
    
    if new_value.isdigit():
        new_value = int(new_value)
    elif new_value.lower() in ['true', 't']:
        new_value = True
    elif new_value.lower() in ['false', 'f']:
        new_value = False
    elif new_value == "":
        new_value = None
        
    updated_patron = collection.update_one({"_id": ObjectId(patron_id)}, {"$set": {field: new_value}})
    if updated_patron.matched_count:
        print(f"\nUpdated patron {patron_id}: {field} = {new_value}")
    else:
        print(f"\nNo patron found with id: {patron_id}")
       
def search():
    fields = {
        "1": "_id",
        "2": "Patron Type Definition",
        "3": "Total Checkouts",
        "4": "Total Renewals",
        "5": "Age Range",
        "6": "Home Library Definition",
        "7": "Circulation Active Month",
        "8": "Circulation Active Year",
        "9": "Notice Preference Definition",
        "10": "Provided Email Address",
        "11": "Year Patron Registered",
        "12": "Within San Francisco County"
    }
    
    print("\nSearchable fields:")
    for k, v in fields.items():
        print(f"{k}. {v}")

    choice = input("Select a field number: ").strip()
    if choice not in fields:
        print("\nInvalid field selection.")
        return

    field = fields[choice]
    value = input("Enter value to search for: ").strip()
    search_type = input("Enter 'exact' or 'like': ").strip().lower()
    
    if value.isdigit():
        value = int(value)
    elif value.lower() in ['true','t']:
        value = True
    elif value.lower() in ['false','f']:
        value = False
    elif field == "_id":
        try:
            value = ObjectId(value)
        except:
            print("\nInvalid ObjectId")
            return
        
    if search_type.lower() == "exact":
        query = {field: value}
    else:
        if field != "_id" and isinstance(value, str): # like search doesn't work on id or int
            query = {field: {"$regex": value, "$options": "i"}}
        else:
            query = {field: value}
        
    results = list(collection.find(query))
    if results:
        clean_print(results)
    else:
        print(f"\nNo results found.")
        
def delete_patron():
    patron_id = input("\nEnter the id of the patron to delete: ").strip()
    deleted = collection.delete_one({"_id": ObjectId(patron_id)})
    
    if deleted.deleted_count:
        print(f"\nPatron with id: {patron_id} successfully deleted.")
    else:
        print(f"\nNo patron found with id: {patron_id}")
        
while True:
    print("1. View all patrons")
    print("2. Add new patron")
    print("3. Update patron info")
    print("4. Search patrons")
    print("5. Delete patron")
    print("6. Exit")
        
    choice = input("Select an option: ").strip()
        
    if choice == "1":
        return_all()
    elif choice == "2":
        add_patron()
    elif choice == "3":
        update_patron()
    elif choice == "4":
        search()
    elif choice == "5":
        delete_patron()
    elif choice == "6":
        break
    else:
        print("Invalid choice.")