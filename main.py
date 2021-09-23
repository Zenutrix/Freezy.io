# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cherrypy
from county import User
from county import Freezy


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    user = User(serial="ABCD1234", username="verbuqqt", credit=5.0, is_admin=True)
    # user.create()
    user = User.from_serial(serial="ABCD1234")
    print(user)
    user.set_credit(20.22)
    print(user)
    cherrypy.quickstart(Freezy())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

