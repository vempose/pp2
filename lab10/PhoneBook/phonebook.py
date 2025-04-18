from config import connect
import csv

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    phone VARCHAR(15) NOT NULL UNIQUE
                )
            """)

def insert_from_csv(file_path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    cur.execute("""
                        INSERT INTO phonebook (first_name, phone)
                        VALUES (%s, %s)
                        ON CONFLICT (phone) DO NOTHING
                    """, row)

def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phonebook (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (first_name, phone))

def update_data(phone, new_first_name=None, new_phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            if new_first_name:
                cur.execute("""
                    UPDATE phonebook SET first_name = %s WHERE phone = %s
                """, (new_first_name, phone))
            if new_phone:
                cur.execute("""
                    UPDATE phonebook SET phone = %s WHERE phone = %s
                """, (new_phone, phone))

def query_data(filter_name=None, filter_phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM phonebook WHERE TRUE"
            params = []
            if filter_name:
                query += " AND first_name ILIKE %s"
                params.append(f"%{filter_name}%")
            if filter_phone:
                query += " AND phone LIKE %s"
                params.append(f"%{filter_phone}%")
            cur.execute(query, params)
            rows = cur.fetchall()
            for row in rows:
                print(row)

def delete_data(first_name=None, phone=None):
    with connect() as conn:
        with conn.cursor() as cur:
            if first_name:
                cur.execute("DELETE FROM phonebook WHERE first_name = %s", (first_name,))
            if phone:
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
