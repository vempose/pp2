from config import connect
import csv

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            # Drop existing functions/procedures if they exist
            cur.execute("""
                DROP FUNCTION IF EXISTS search_by_pattern(text);
                DROP PROCEDURE IF EXISTS upsert_contact(varchar, varchar);
                DROP PROCEDURE IF EXISTS bulk_insert_contacts(text[][], integer, integer);
                DROP FUNCTION IF EXISTS get_paginated_contacts(integer, integer);
                DROP PROCEDURE IF EXISTS delete_contact(varchar, varchar);
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    phone VARCHAR(15) NOT NULL UNIQUE
                )
            """)

            cur.execute("""
                CREATE OR REPLACE FUNCTION search_by_pattern(search_pattern TEXT)
                RETURNS TABLE (id INTEGER, first_name VARCHAR, phone VARCHAR) AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT phonebook.id, phonebook.first_name, phonebook.phone 
                    FROM phonebook
                    WHERE phonebook.first_name ILIKE '%' || search_pattern || '%' 
                       OR phonebook.phone LIKE '%' || search_pattern || '%';
                END;
                $$ LANGUAGE plpgsql;
            """)
            conn.commit()

            cur.execute("""
                CREATE OR REPLACE PROCEDURE upsert_contact(
                    p_name VARCHAR, 
                    p_phone VARCHAR
                ) AS $$
                BEGIN
                    INSERT INTO phonebook (first_name, phone)
                    VALUES (p_name, p_phone)
                    ON CONFLICT (phone) 
                    DO UPDATE SET first_name = EXCLUDED.first_name;
                END;
                $$ LANGUAGE plpgsql;
            """)

            cur.execute("""
                CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
                    users TEXT[][],
                    INOUT inserted_count INTEGER DEFAULT 0,
                    INOUT invalid_count INTEGER DEFAULT 0
                ) AS $$
                DECLARE
                    user_record TEXT[];
                BEGIN
                    inserted_count := 0;
                    invalid_count := 0;
                    
                    FOREACH user_record SLICE 1 IN ARRAY users
                    LOOP
                        IF user_record[2] ~ '^[0-9]+$' THEN
                            INSERT INTO phonebook (first_name, phone)
                            VALUES (user_record[1], user_record[2])
                            ON CONFLICT (phone) DO NOTHING;
                            
                            IF FOUND THEN
                                inserted_count := inserted_count + 1;
                            END IF;
                        ELSE
                            invalid_count := invalid_count + 1;
                        END IF;
                    END LOOP;
                END;
                $$ LANGUAGE plpgsql;
            """)

            cur.execute("""
                CREATE OR REPLACE FUNCTION get_paginated_contacts(
                    lim INTEGER,
                    offs INTEGER
                ) RETURNS TABLE (id INTEGER, first_name VARCHAR, phone VARCHAR) AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT phonebook.id, phonebook.first_name, phonebook.phone
                    FROM phonebook 
                    ORDER BY id
                    LIMIT lim OFFSET offs;
                END;
                $$ LANGUAGE plpgsql;
            """)
            conn.commit()

            cur.execute("""
                CREATE OR REPLACE PROCEDURE delete_contact(
                    p_name VARCHAR DEFAULT NULL,
                    p_phone VARCHAR DEFAULT NULL
                ) AS $$
                BEGIN
                    IF p_name IS NOT NULL THEN
                        DELETE FROM phonebook WHERE first_name = p_name;
                    END IF;
                    IF p_phone IS NOT NULL THEN
                        DELETE FROM phonebook WHERE phone = p_phone;
                    END IF;
                END;
                $$ LANGUAGE plpgsql;
            """)
            conn.commit()

def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (first_name, phone))
            conn.commit()
            print("Contact added/updated successfully")

def insert_from_csv(file_path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                users = [row for row in reader if len(row) >= 2]
                
                inserted, invalid = 0, 0
                cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (users, inserted, invalid))
                result = cur.fetchone()
                print(f"Inserted {result[0]} contacts")
                if result[1] > 0:
                    print(f"{result[1]} contacts had invalid phone numbers")
                conn.commit()

def update_data(phone, new_name=None, new_phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute(
                    "UPDATE phonebook SET first_name = %s WHERE phone = %s",
                    (new_name, phone)
                )
            if new_phone:
                cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE phone = %s",
                    (new_phone, phone)
                )
            conn.commit()
            print("Contact updated successfully")

def query_data(name=None, phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM phonebook WHERE TRUE"
            params = []
            if name:
                query += " AND first_name ILIKE %s"
                params.append(f"%{name}%")
            if phone:
                query += " AND phone LIKE %s"
                params.append(f"%{phone}%")
            
            cur.execute(query, params)
            contacts = cur.fetchall()
            
            if not contacts:
                print("No contacts found")
            else:
                print("\nContacts:")
                for contact in contacts:
                    print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}")

def query_by_pattern(pattern):
    with connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
                contacts = cur.fetchall()
                
                if not contacts:
                    print("No contacts found matching the pattern")
                else:
                    print("\nMatching contacts:")
                    for contact in contacts:
                        print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}")
            except Exception as e:
                print(f"Error searching contacts: {e}")

def query_with_pagination(limit, offset):
    with connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT * FROM get_paginated_contacts(%s, %s)", (limit, offset))
                contacts = cur.fetchall()
                
                if not contacts:
                    print("No contacts found in this range")
                else:
                    print("\nContacts:")
                    for contact in contacts:
                        print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}")
            except Exception as e:
                print(f"Error fetching paginated contacts: {e}")

def delete_data(name=None, phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s, %s)", (name, phone))
            conn.commit()
            print("Contact(s) deleted successfully")

def insert_many_from_console():
    contacts = []
    print("\nEnter contacts (leave name blank to finish):")
    while True:
        name = input("Name: ").strip()
        if not name:
            break
        phone = input("Phone: ").strip()
        contacts.append([name, phone])
    
    if not contacts:
        print("No contacts to add")
        return
    
    with connect() as conn:
        with conn.cursor() as cur:
            inserted, invalid = 0, 0
            cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (contacts, inserted, invalid))
            result = cur.fetchone()
            print(f"\nSuccessfully inserted {result[0]} contacts")
            if result[1] > 0:
                print(f"{result[1]} contacts had invalid phone numbers")
            conn.commit()