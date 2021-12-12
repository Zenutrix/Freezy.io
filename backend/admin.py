import logging
import sys

import requests as requests

import backend.card_reader
from backend import User

LOG_FORMAT_CONSOLE = "[%(levelname)s] %(message)s"


def get_serial():
    import RPi.GPIO
    import mfrc522
    serial = None
    try:
        logger.debug("Initializing mfrc522 reader")
        mifare_reader = mfrc522.MFRC522()
        status = None
        logger.info("Hold a tag near the reader")
        while status is not mifare_reader.MI_OK:
            (s, t) = mifare_reader.MFRC522_Request(mifare_reader.PICC_REQIDL)
            status = s

        logger.info("Card detected, trying to read serial from it")
        (status, uid) = mifare_reader.MFRC522_Anticoll()
        if status == mifare_reader.MI_OK:
            serial = hex(uid[0]) + ':' + hex(uid[1]) + ':' + hex(uid[2]) + ':' + hex(uid[3])
            logger.info('Reading uid was successful.')
            # logger.info('  - uid:' + uid[0] + ":" + uid[1] + ":" + uid[2] + ":" + uid[3])
            logger.info('  - serial: ' + serial)
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt")
        exit()
    except Exception as e:
        logger.error("Error: ", e)
        exit()
    finally:
        logger.debug("Cleaning up GPIO")
        RPi.GPIO.cleanup()
        return serial


def get_username():
    username = input("Enter the new users name: ")
    if username:
        return username
    else:
        logger.error("Username can't be empty")
        exit()


def get_credit():
    credit = 0.00
    try:
        c_in = input("Enter the new users credit [0]: ")
        if c_in:
            credit = float(c_in)
    except ValueError:
        logger.error("Invalid value, try again")
        return get_credit()
    return credit


def get_is_admin():
    is_admin = False
    a_in = input("Enter if the new user is an admin [False]: ")
    if a_in == '1' or a_in.lower() == "true":
        is_admin = True
    return is_admin


def create_tables():
    backend.database.create_tables()


if __name__ == '__main__':

    def print_help():
        logger.info("Usage: python3 -m backend.admin [COMMAND] [PARAMETERS]")
        logger.info("  python3 -m backend.admin create_tables")
        logger.info("  python3 -m backend.admin adduser")
        # print("  python3 -m backend.admin deluser")
        logger.info("  python3 -m backend.admin print_serial")

    def add_user():
        username = get_username()
        credit = get_credit()
        is_admin = get_is_admin()
        serial = get_serial()
        if username and serial:
            new_user = User(username=username, serial=serial, credit=credit, is_admin=is_admin)
            try:
                new_user.create()
                logger.info("New User created")
            except:
                logger.error("Something went wrong with the database")
                logger.error("Most likely a user with this MIFARE-Tag already exists")
        else:
            logger.error("Something went wrong")


    logging.basicConfig(format=LOG_FORMAT_CONSOLE)
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)
    try:
        logger.info("Checking if webserver is running...")
        r = requests.get('http://127.0.0.1:8080/api/')
        logger.error("Shut down the webserver before using the admin script!")
        exit()
    except requests.exceptions.ConnectionError:
        logger.info("webserver is offline, admin script is ready to run")

    print()

    if len(sys.argv) == 1:
        print_help()
    if len(sys.argv) == 2:
        if sys.argv[1] == 'create_tables':
            create_tables()
        elif sys.argv[1] == 'help':
            print_help()
        elif sys.argv[1] == 'adduser':
            # logger.info("Adding User...")
            add_user()
        elif sys.argv[1] == 'deluser':
            print("Deleting User...")
            # TODO delete user by name/serial
        elif sys.argv[1] == 'printserial':
            get_serial()