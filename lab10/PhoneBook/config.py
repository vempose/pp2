import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook",
        user="username",
        password="password"
    )
