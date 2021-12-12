import cherrypy
import cherrypy_cors
import backend.database

from backend import Freezy, start_reader

debug = False
app = cherrypy.tree.mount(Freezy(), '/api/')
app.toolboxes['cors'] = cherrypy_cors.tools

if __name__ == '__main__':
    cherrypy.config.update({
        'cors.expose.on': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })

    try:
        start_reader(debug=debug)
        cherrypy.quickstart(app)
    except KeyboardInterrupt:
        backend.database.close()
        print("closing db connection")