from phonebook import *

def menu():
    create_table()

    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Insert single contact")
        print("2. Insert multiple contacts")
        print("3. Import from CSV")
        print("4. Update contact")
        print("5. Search contacts")
        print("6. Search by pattern")
        print("7. List with pagination")
        print("8. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_many_from_console()
        elif choice == '3':
            path = input("Enter CSV file path: ").strip()
            insert_from_csv(path)
        elif choice == '4':
            phone = input("Enter current phone number: ").strip()
            new_name = input("New name (leave blank to keep): ").strip() or None
            new_phone = input("New phone (leave blank to keep): ").strip() or None
            update_data(phone, new_name, new_phone)
        elif choice == '5':
            name = input("Filter by name (leave blank for all): ").strip() or None
            phone = input("Filter by phone (leave blank for all): ").strip() or None
            query_data(name, phone)
        elif choice == '6':
            pattern = input("Enter search pattern: ").strip()
            query_by_pattern(pattern)
        elif choice == '7':
            try:
                limit = int(input("Items per page: "))
                offset = int(input("Offset: "))
                query_with_pagination(limit, offset)
            except ValueError:
                print("Please enter valid numbers")
        elif choice == '8':
            name = input("Delete by name (leave blank to skip): ").strip() or None
            phone = input("Delete by phone (leave blank to skip): ").strip() or None
            delete_data(name, phone)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again")

if __name__ == '__main__':
    menu()