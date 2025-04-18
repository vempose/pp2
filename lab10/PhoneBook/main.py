from phonebook import *

def menu():
    create_table()

    while True:
        print("\n-- PhoneBook Menu")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            phone = input("Enter current phone number: ")
            new_name = input("New name (or leave blank): ") or None
            new_phone = input("New phone (or leave blank): ") or None
            update_data(phone, new_name, new_phone)
        elif choice == '4':
            name = input("Filter by name (or leave blank): ") or None
            phone = input("Filter by phone (or leave blank): ") or None
            query_data(name, phone)
        elif choice == '5':
            name = input("Delete by name (or leave blank): ") or None
            phone = input("Delete by phone (or leave blank): ") or None
            delete_data(name, phone)
        elif choice == '0':
            break
        else:
            print("X Invalid option")

if __name__ == '__main__':
    menu()
