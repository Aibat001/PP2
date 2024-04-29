import psycopg2
from config import *

#connecting to our database
conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

#creating table if not exists
conn.autocommit = True
cursor = conn.cursor()
cursor.execute(
"""CREATE TABLE phonebook(
    Name text PRIMARY KEY,
    number text NOT NULL);"""
    )

cursor.close()
conn.close()