import psycopg2
import csv
from config import *

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor()

# Insert data into phonebook table (option 1: from CSV file)
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            name, number = row
            cur.execute(
                'INSERT INTO phonebook(name,number) VALUES(%s,%s)',
                (name, number)
            )


# Insert data into phonebook table (option 2: from console)
def insert_data_from_console():
    name = input("Enter name: ")
    number = input("Enter phone: ")
    cur.execute(
        'INSERT INTO phonebook(name,number) VALUES(%s,%s)',
        (name, number)
    )
    conn.commit()
    print("Data uploaded successfully from console.")


# Update data in phonebook table
def update_data():
    name = input("Enter the name of the user to update: ")
    field = input("Enter the field to update (name/phone): ")
    value = input("Enter the new value: ")
    if field == "name":
        cur.execute(
            "UPDATE phonebook SET name = %s WHERE name = %s",
            (value, name)
        )
    elif field == "phone":
        cur.execute(
            "UPDATE phonebook SET number = %s WHERE name = %s",
            (value, name)
        )
    conn.commit()
    print("Data updated successfully.")


# Query data from phonebook table
def query_data():
    field = input("Enter the field to query (name/number/all): ")
    if field == "name":
        name = input("Enter the name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE name = %s",
            (name,)
        )
    elif field == "number":
        phone = input("Enter the phone: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE number = %s",
            (phone,)
        )
    elif field == "all":
        cur.execute("SELECT * FROM phonebook")
    else:
        print("Invalid input.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)


# Delete data from phonebook table
def delete_data():
    field = input("Enter the field to delete by (name/number): ")
    value = input("Enter the value: ")
    if field == "name":
        cur.execute(
            "DELETE FROM phonebook WHERE name = %s",
            (value,)
        )
    elif field == "number":
        cur.execute(
            "DELETE FROM phonebook WHERE number = %s",
            (value,)
        )
    conn.commit()
    print("Data deleted successfully.")


# Main program loop
while True:
    print("phonebook options:")
    print("1. Insert data from CSV file.")
    print("2. Insert data from console.")
    print("3. Update data.")
    print("4. Query data.")
    print("5. Delete data.")
    print("0. Exit.")
    choice = input("Enter your choice: ")
    if choice == "1":
        filename = input("Enter the filename:")
        insert_from_csv(filename)
    elif choice == "2":
        insert_data_from_console()
    elif choice == "3":
        update_data()
    elif choice == "4":
        query_data()
    elif choice == "5":
        delete_data()
    elif choice == "0":
        break
    else:
        print("Invalid input. Please enter a valid option.")
conn.commit()
cur.close()
conn.close()