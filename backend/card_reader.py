# TODO read Serial
import threading
import time
import backend.core as core

debug_serial = "0x3d:0xe4:0x12:0x62"
debug_sleep = 5


def debug_loop():
    while True:
        if not core.get_current_user():
            print('Pretending to read debug_serial in ' + str(debug_sleep))
            time.sleep(debug_sleep)
            print("'Reading' " + debug_serial)
            core.set_user_by_serial(debug_serial)


def read_loop():
    import mfrc522
    mifare_reader = mfrc522.MFRC522()
    while mifare_reader:
        (status, TagType) = mifare_reader.MFRC522_Request(mifare_reader.PICC_REQIDL)

        if status == mifare_reader.MI_OK:
            print("Card detected", status, TagType)

        (status, uid) = mifare_reader.MFRC522_Anticoll()

        if status == mifare_reader.MI_OK:
            serial = hex(uid[0]) + ':' + hex(uid[1]) + ':' + hex(uid[2]) + ':' + hex(uid[3])
            print('MIFARE device detected. serial:' + serial)
            core.set_user_by_serial(serial)


def start(debug=False):
    if debug:
        print('Starting debug MIFARE Reader')
        debug_thread = threading.Thread(target=debug_loop, name="DEBUG-READER", daemon=True)
        debug_thread.start()
    else:
        print('Starting MIFARE Reader')
        read_thread = threading.Thread(target=read_loop, name="MIFARE-READER", daemon=True)
        read_thread.start()
