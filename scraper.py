import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from datetime import date

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

def populate_product(conn, product_obj):
    """ populates product table in SQLite """
    sql = ''' INSERT INTO product(name,type)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product_obj)
    conn.commit()
    return cur.lastrowid

def find_product(conn, name):
    """ checks if product exists in SQLite """
    cur = conn.cursor()
    cur.execute("""SELECT id
                   FROM product
                   WHERE name=?""",
                (name))
    return cur.fetchone()

def populate_price(conn, item_id, price):
    """ populates price table in SQLite """
    sql = ''' INSERT INTO price(item_id,price,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    price = "R"+str(price)
    cur.execute('''INSERT INTO price(item_id,price,date)
        VALUES(?,?,?)''',(str(item_id),price,date.today(),))
    conn.commit()
    return cur.lastrowid

def scraper(URL, conn, product_type):
    """ scrapes website for titles and prices """
    print("Scraping "+product_type+"s")
    page = requests.get(URL)
    page = BeautifulSoup(page.content, 'html.parser')
    results = page.find(id='rgt-cnt')
    products = results.find_all('div', class_='product-inner')

    for product in products:
        product_name = product.find('img')
        product_price = product.find('div', class_='price')

        product_name = product_name['alt']
        product_price = ''.join(filter(str.isdigit, product_price.text.strip()))

        product_obj = product_name,
        product_id = find_product(conn, product_obj)
        if product_id == None:
            product_obj = product_name, product_type
            populate_product(conn, product_obj)
        else:
            populate_price(conn, product_id[0], product_price)

# Graphics cards: https://www.evetech.co.za/components/nvidia-ati-graphics-cards-21.aspx
# Monitors: https://www.evetech.co.za/PC-Components/pc-monitors-89.aspx

sql_create_product_table = """ CREATE TABLE IF NOT EXISTS product (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    type text NOT NULL
                                );"""
sql_create_price_table = """ CREATE TABLE price (
                                    `id`	integer,
                                    `item_id`	integer NOT NULL,
                                    `price`	text NOT NULL,
                                    `date`	TEXT,
                                    PRIMARY KEY(`id`)
                                );"""

database = "evetech.db"
conn = create_connection(database)
if conn is not None:
    create_table(conn, sql_create_product_table)
    create_table(conn, sql_create_price_table)
else:
    print("Error! cannot create the database connection.")

URL = 'https://www.evetech.co.za/components/nvidia-ati-graphics-cards-21.aspx'
scraper(URL, conn, "gpu")

URL = 'https://www.evetech.co.za/PC-Components/pc-monitors-89.aspx'
scraper(URL, conn, "monitor")

URL = 'https://www.evetech.co.za/components/ddr3-gaming-ram-modules-20.aspx'
scraper(URL, conn, "ram")
