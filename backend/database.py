from time import sleep

import mysql.connector
from mysql.connector import errorcode

# Login Data
# TODO load from config | hard coded no good
HOST = "localhost"
USERNAME = "freezy"
PASSWORD = "password"
DATABASE = "freezy"
PORT = 3306


def create_tables():
    cursor = connection.cursor()
    create_tables_sql = open("backend/sql/tables.sql").read()
    connection.connect()
    cursor.execute(create_tables_sql, multi=True)


# establish connection, handle errors
try:
    connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD, database=DATABASE)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if connection:
        create_tables()


# sets a value in a table at identifier
#
# creates a cursor with current connection
# executes SQL statement
# commits changes to db
def set_value(table, value_name, value, identifier, id_value):
    c = connection.cursor()
    c.execute("UPDATE %s SET %s='%s' WHERE %s=%s;" % (table, value_name, value, identifier, id_value))
    connection.commit()


def close():
    connection.close()