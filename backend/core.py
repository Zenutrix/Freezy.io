from backend import database, models

_current_user = None


def set_user_by_serial(serial):
    for user in models.get_users():
        if user.serial == serial:
            global _current_user
            user.reload()
            _current_user = user
            print("user found")


def get_current_user():
    return _current_user


def get_drinks_json():
    return [x.to_json() for x in models.get_drinks()]


def get_users_json():
    return [x.to_json() for x in models.get_users()]


# TODO remove? unused at the time, required for admin panel


# drink list for logging later on
def purchase(current_user, total, unsafe_drinks):
    new_credit = current_user.credit - total
    print(new_credit)
    database.connection.connect()
    c = database.connection.cursor()  # create cursor
    c.execute(open('backend/sql/make_purchase.sql').read(-1), {'new_credit': new_credit, 'user_id': current_user.user_id})
    database.connection.commit()
    current_user.reload()


def logout():
    global _current_user
    del _current_user
    _current_user = None