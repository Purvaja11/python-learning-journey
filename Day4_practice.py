#Exercise 1
#Word frequency counter
# Count how many times each word appears in a sentence
sentence = "python is amazing and python is powerful and python is fun"
words = sentence.split()

unique_words = []
for word in words:
    if word not in unique_words:
        unique_words.append(word)

print("Word frequencies:")
for word in unique_words:
    count = words.count(word)
    print(f"  '{word}' : {count} times")

#Exercise 2 
#Phone Book
# Create a phone book dictionary
# Add 3 contacts
# Search for a contact
# Update a phone number
# Delete a contact
phone_book = {}


def add_number():
    print("\n---ADD A CONTACT---")
    #generate name id
    if phone_book:
        name_id = max(phone_book.keys()) + 1
    else:
        name_id = 1
    #Get info
    name = input("Name: ").strip().title()
    while True:
        number = (input("Number: "))
        if number.isdigit() and len(number) == 10:
            number = int(number)
            break
        print("Invalid Number! Please enter 10 numbers")

    #store in database
    phone_book[name_id] = {
        "name" : name,
        "number" : number
    }

    print(f"\nContact added successfully! ID: {name_id}")

def search_number():
    print("\n---SEARCH STUDENT---")
    print("1. Search by ID ")
    print("2. Search by Name ")

    choice = input("Choose (1/2): ")

    if choice == "1":
        name_id = input("Enter Phone ID: ")
        if name_id.isdigit() and int(name_id) in phone_book:
            name_id = int(name_id)
            display_contact_details(name_id)
        else:
            print("Contact not found!")

    elif choice == "2":
        search_name = input("Enter name: ").strip().title()
        found = False
        for name_id, info in phone_book.items():
            if info["name"] == search_name:
                display_contact_details(name_id)
                found = True
                break
        if not found:
            print("Contact not found!")
    
    else:
        print("Invalid choice!")


def display_contact_details(name_id):
    info = phone_book[name_id]

    print("\n"+ "="*40)
    print("CONTACT DETAILS")
    print("="*40)
    print(f"ID: {name_id}")
    print(f"Name: {info['name']}")
    print(f"Number: {info['number']}")

def update_contact_details():
    print("---UPDATE DETAILS---")
    print("1. Update by ID")
    print("2. Update by Name")

    choice = input("Choose (1/2): ")

    if choice == "1":
        name_id = input("Enter Phone ID: ") 
        if name_id.isdigit() and int(name_id) in phone_book:
            name_id = int(name_id)
            new_number = int(input("Enter New Number:"))
            phone_book[name_id]["number"] = new_number
            print("Contact Updated Successfully!")
        else:
            print("Contact not found!")
    
    elif choice == "2":
        update_name = input("Enter Name: ").strip().title()
        found = False
        for name_id, info in phone_book.items():
            if info ["name"] == update_name:
                new_number = int(input("Enter New Number:"))
                phone_book[name_id]["number"] = new_number
                print("Contact Updated Successfully!")
                found = True
                break
        if not found:
            print("Contact not found!")

def delete_contact_details():
    print("---DELETE DETAILS---")
    print("1. Delete by ID")
    print("2. Delete by Name")

    choice = input("Choose (1/2): ")

    if choice == "1":
        name_id = input("Enter Phone ID: ") 
        if name_id.isdigit() and int(name_id) in phone_book:
            name_id = int(name_id)
            phone_book.pop(name_id)
            print("Contact Deleted Successfully!")

        else:
            print("Contact not found!")

    elif choice == "2":
        deleted_name = input("Enter Name: ").strip().title()
        name_to_delete = None

        for name_id, info in phone_book.items():
            if info["name"] == deleted_name:
                name_to_delete = name_id
                break
        
        if name_to_delete:
            phone_book.pop(name_to_delete)
            print("Contact Deleted Successfully!")
        else:
            print("Contact not found!")


def display_all_contacts():
    if not phone_book:
        print("\nX No contacts in database!")
        return
    
    print("\n" + "="*60)
    print("ALL CONTACTS")
    print("="*60)

    for name_id, info in phone_book.items():
        print(f"\nID: {name_id}")
        print(f"  Name: {info['name']}")
        print(f"  Phone Number: {info['number']}")

while True:
    print("\n" + "="*60)
    print("MENU")
    print("="*60)
    print("1. Add Contacts")
    print("2. Display all contacts")
    print("3. Search a Contact")
    print("4. Update Phone Number")
    print("5. Delete a Contact")
    print("6. Exit")

    choice = input("\nChoose an option (1-6): ")

    if choice == "1":
        add_number()
    elif choice == "2":
        display_all_contacts()
    elif choice == "3":
        search_number()
    elif choice == "4":
        update_contact_details()
    elif choice == "5":
        delete_contact_details()
    elif choice == "6":
        print("\n👋 GOODBYE!")
        break


#Exercise 3
# Find students enrolled in both Math and Science
# Find: common students, only math, only science, all students
math_students = {"Alice", "Bob", "Charlie", "Diana"}
science_students = {"Bob", "Diana", "Eve", "Frank"}

common_students = math_students & science_students
only_math = math_students - science_students
only_science = science_students - math_students
all_students = math_students | science_students

print("Practice for SETS")
print(f"\nCommon Students: {common_students}")
print(f"Only Math Students: {only_math}")
print(f"Only Science Students: {only_science}")
print(f"All Students: {all_students}")
