import cherrypy
import cherrypy_cors
from backend import Freezy, User, start_reader

debug = False
app = cherrypy.tree.mount(Freezy(), '/api/')
app.toolboxes['cors'] = cherrypy_cors.tools


def debug_user():
    # 61,228,18,98
    ser = str(hex(61)) + ':' + str(hex(228)) + ':' + str(hex(18)) + ':' + str(hex(98))
    user = User(serial=ser, username="verbuqqt", credit=5.0, is_admin=True)
    # user.create()
    user = User.from_serial(serial=ser)
    print(user)
    user.set_credit(20)
    print(user)


if __name__ == '__main__':
    import backend.database
    cherrypy.config.update({
        'cors.expose.on': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })

    if debug:
        debug_user()
    try:
        start_reader(debug=debug)
        cherrypy.quickstart(app)
    except KeyboardInterrupt:
        backend.database.close()
        print("closing db connection")