import mysql.connector
from mysql.connector import errorcode

# Login Data
# TODO load from config | hard coded no good
HOST = "localhost"
USERNAME = "freezy"
PASSWORD = "shittyfreez/dev"
DATABASE = "freezy"
PORT = 3306


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
else:
    # create tables
    cursor = connection.cursor()
    create_tables = open("backend/sql/tables.sql").read()
    cursor.execute(create_tables, multi=True)


# sets a value in a table at identifier
#
# creates a cursor with current connection
# executes SQL statement
# commits changes to db
def set_value(table, value_name, value, identifier, id_value):
    c = connection.cursor()
    c.execute("UPDATE %s SET %s='%s' WHERE %s=%s;" % (table, value_name, value, identifier, id_value))
    connection.commit()


def get_value(table, value_name, value):
    pass