import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database """
    print('Initializing DB')
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def list_products(conn):
    print('Listing products')
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    for product in products:
        print(str(product[0]) + "    " + product[1] + "    " + product[2])

def select_product(conn):
    id = input("Enter ID: ") 
    cur = conn.cursor()
    id = int(id),
    cur.execute("SELECT * FROM price WHERE item_id=?",(id))
    products = cur.fetchall()
    for product in products:
        print(str(product[0]) + "    " + str(product[1]) + "    " + product[2])
        # print("found")

sql_create_product_table = """ CREATE TABLE IF NOT EXISTS product (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    type text NOT NULL
                                );"""
sql_create_price_table = """ CREATE TABLE IF NOT EXISTS price (
                                    id integer PRIMARY KEY,
                                    item_id integer NOT NULL,
                                    price text NOT NULL
                                );"""

database = "evetech.db"
conn = create_connection(database)
if conn is not None:
    create_table(conn, sql_create_product_table)
    create_table(conn, sql_create_price_table)
else:
    print("Error! cannot create the database connection.")

list_products(conn)
select_product(conn)