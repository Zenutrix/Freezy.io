from backend import database

_drinks = {}
_users = {}


def cache_data():
    database.connection.connect()
    c = database.connection.cursor()  # create cursor
    c.execute(open('backend/sql/get_all_users.sql').read(-1))
    for user_id, serial, username, credit, is_admin in c:
        user = User(serial, username, credit, is_admin, user_id)
        _users[user.user_id] = user

    c = database.connection.cursor()  # create cursor
    c.execute(open('backend/sql/get_all_drinks.sql').read(-1))
    for drink_id, drink_name, price, description in c:
        drink = Drink(drink_id, drink_name, price, description)
        _drinks[drink.drink_id] = drink


def get_users():
    return _users.values()


def get_drinks():
    return _drinks.values()


def get_drink_by_id(drink_id):
    return _drinks.get(drink_id)


class Drink:
    def __init__(self, drink_id, drink_name, price, description):
        self.drink_id = drink_id
        self.drink_name = drink_name
        self.price = price
        self.description = description

    # TODO classmethod from_id()

    def to_json(self):
        return {
            'drink_id': self.drink_id,
            'drink_name': self.drink_name,
            'price': self.price,
            'description': self.description,
        }

    # load the drinkdata from the database by executing an sql statement and returning the results as a dict
    def _load_from_db(self):
        database.connection.connect()  # connect to db
        c = database.connection.cursor()  # create cursor
        c.execute("""SELECT drink_id, drink_name, price, description FROM drinks WHERE drink_id='%s'""" % self.drink_id)
        for user_id, name, credit, is_admin in c:
            c.close()
            return {"user_id": user_id, "name": name, "credit": credit, "is_admin": is_admin}

    def _update_field(self, field):
        database.connection.connect()
        c = database.connection.cursor()
        c.execute("SELECT %s FROM drinks WHERE drink_id=%s" % (field, self.drink_id))
        self.__setattr__(field, c.fetchone()[0])

    def create(self):
        database.connection.connect()
        c = database.connection.cursor()
        c.execute('''INSERT INTO drinks (drink_name, price, description) VALUES (%s, %s, %s)''',
                  (self.drink_name, self.price, self.description))
        database.connection.commit()
        c.close()


class User:
    def __init__(self, serial, username, credit, is_admin, user_id=None):
        self.user_id = user_id
        self.serial = serial
        self.username = username
        self.credit = credit
        self.is_admin = is_admin

    def to_json(self):
        return {
            'user_id': self.user_id,
            'serial': self.serial,
            'username': self.username,
            'credit': self.credit,
            'is_admin': self.is_admin,
        }

    def __str__(self):
        return "<User> id:%s, serial:%s, name:%s, credit:%s, is_admin:%s>" % (
            self.user_id, self.serial, self.username, self.credit, self.is_admin)

    @classmethod
    def from_serial(cls, serial):
        cls.serial = serial
        userdata = cls._load_from_db(cls)
        return cls(user_id=userdata['user_id'], serial=serial, username=userdata['username'], credit=userdata['credit'],
                   is_admin=userdata['is_admin'])

    # load the userdata from the database by executing an sql statement and returning the results as a dict
    def _load_from_db(self):
        database.connection.connect()  # connect to db
        c = database.connection.cursor()  # create cursor
        c.execute("""SELECT user_id, username, credit, is_admin FROM users WHERE serial='%s'""" % self.serial)
        for user_id, username, credit, is_admin in c:
            return {"user_id": user_id, "username": username, "credit": credit, "is_admin": is_admin}

    def reload(self):
        database.connection.connect()  # connect to db
        c = database.connection.cursor()  # create cursor
        c.execute("""SELECT username, credit, is_admin FROM users WHERE serial='%s'""" % self.serial)
        for username, credit, is_admin in c:
            self.username = username
            self.credit = credit
            self.is_admin = is_admin

    def _update_field(self, field):
        database.connection.connect()
        c = database.connection.cursor()
        c.execute("SELECT %s FROM users WHERE user_id=%s" % (field, self.user_id))
        self.__setattr__(field, c.fetchone()[0])

    def create(self):
        database.connection.connect()
        c = database.connection.cursor()
        c.execute('''INSERT INTO users (serial, username, credit, is_admin) VALUES (%s, %s, %s, %s)''',
                  (self.serial, self.username, self.credit, self.is_admin))
        database.connection.commit()
        c.close()

    def set_name(self, new_name):
        database.set_value("users", "username", new_name, "user_id", self.user_id)
        self._update_field("name")

    def set_credit(self, new_credit):
        database.set_value("users", "credit", new_credit, "user_id", self.user_id)
        self._update_field("credit")

    def set_admin(self, is_admin):
        database.set_value("users", "is_admin", is_admin, "user_id", self.user_id)
        self._update_field("is_admin")


cache_data()
